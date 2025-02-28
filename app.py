import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 🚀 Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# 🎨 Ajustes Visuais com CSS
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            min-width: 280px;
            width: 280px;
        }
        .block-container {
            padding-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# 🔄 Carregar os dados e atualizar automaticamente a cada 10 minutos
@st.cache_data(ttl=600)  
def load_data():
    CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"
    return pd.read_csv(CSV_URL)

df = load_data()

# 🔄 Botão para atualizar os dados manualmente
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# ✅ Remover colunas duplicadas e formatar dados
df = df.loc[:, ~df.columns.duplicated()].copy()
df["release_date"] = df["release_date"].replace({None: "Indefinido", "nan": "Indefinido", "NaT": "Indefinido"}).astype(str)
df["price"] = df["price"].replace({None: "Indefinido", "nan": "Indefinido", "NaT": "Indefinido"}).astype(str)

# 🔍 Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# 🎯 Entrada do Usuário: Nome dos jogos favoritos
jogos_favoritos = st.sidebar.text_area("🎯 Digite os jogos que você gosta (separados por vírgula):")

# 🔎 Buscar Gêneros dos Jogos Favoritos
@st.cache_data
def buscar_generos(jogos):
    """Busca os gêneros dos jogos digitados usando a API da Steam"""
    generos_favoritos = set()
    steam_url = "https://store.steampowered.com/api/appdetails?appids={}"

    for jogo in jogos:
        jogo = jogo.strip().lower()
        
        # 🔍 Simulação de busca de App ID (idealmente usar um dataset)
        app_id = buscar_app_id(jogo)  # Função para buscar App ID

        if app_id:
            response = requests.get(steam_url.format(app_id))
            data = response.json()

            if str(app_id) in data and "data" in data[str(app_id)]:
                generos = data[str(app_id)]["data"].get("genres", [])
                generos_favoritos.update([g["description"] for g in generos])

    return list(generos_favoritos)

# 🕹️ Função para buscar App ID (pode ser um dataset local)
def buscar_app_id(nome_jogo):
    """Simula a busca do App ID de um jogo (use um dataset real)"""
    dataset_jogos = {
        "elden ring": 1245620,
        "hades": 1145360,
        "stardew valley": 413150,
        "counter-strike 2": 730,
        "cyberpunk 2077": 1091500
    }
    return dataset_jogos.get(nome_jogo.lower())

# 🔄 Aplicar Filtro com Base nos Gêneros Identificados
if jogos_favoritos:
    lista_jogos = jogos_favoritos.split(",")
    generos_encontrados = buscar_generos(lista_jogos)

    if generos_encontrados:
        df = df[df["Gêneros"].apply(lambda x: any(g in x for g in generos_encontrados))]
        st.sidebar.success(f"🎯 Filtrando por gêneros: {', '.join(generos_encontrados)}")

# 🔍 Filtro por Nome
nome_busca = st.sidebar.text_input("🔎 Buscar jogo por nome:")
if nome_busca:
    df = df[df["title"].str.contains(nome_busca, case=False, na=False)]

# 🔍 Filtro por Gênero
if "genres" in df.columns:
    df["Gêneros_Filtro"] = df["genres"].fillna("").astype(str)
    generos_exploded = sorted(set(g for sublist in df["Gêneros_Filtro"].str.split(', ') for g in sublist))
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", generos_exploded)
    if genero_selecionado:
        df = df[df["Gêneros_Filtro"].apply(lambda x: all(g in x for g in genero_selecionado))]

# 🔍 Filtro por Data de Lançamento
min_date = pd.to_datetime(df["release_date"], errors='coerce').min()
max_date = pd.to_datetime(df["release_date"], errors='coerce').max()
data_selecionada = st.sidebar.date_input("Filtrar por data de lançamento:", [min_date, max_date], min_value=min_date, max_value=max_date)
if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
    df = df[(pd.to_datetime(df["release_date"], errors='coerce') >= pd.to_datetime(data_selecionada[0])) &
            (pd.to_datetime(df["release_date"], errors='coerce') <= pd.to_datetime(data_selecionada[1]))]

# 🔍 Filtro por Preço
unique_prices = sorted(df["price"].dropna().unique(), key=lambda x: (x.isdigit(), x))
preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", unique_prices)
if preco_selecionado:
    df = df[df["price"].isin(preco_selecionado)]

# 🔍 Filtro para Jogos Gratuitos
if st.sidebar.checkbox("🆓 Mostrar apenas jogos gratuitos"):
    df = df[df["price"].str.lower().str.contains("free", na=False)]

# 🔍 Filtro para Jogos com Link
if st.sidebar.checkbox("🔗 Mostrar apenas jogos com link"):
    df = df[df["game_url"].notna()]

# 🔥 Destaque para Jogos Próximos ao Lançamento
hoje = datetime.today()
prox_7_dias = hoje + timedelta(days=7)
df["Destaque"] = pd.to_datetime(df["release_date"], errors='coerce').apply(
    lambda x: "🔥 " if pd.notna(x) and x >= hoje and x <= prox_7_dias else "")

df["Nome"] = df["Destaque"] + df["title"]

if st.sidebar.checkbox("🔥 Mostrar apenas lançamentos próximos"):
    df = df[df["Destaque"].str.contains("🔥", na=False)]

# 📌 Ordenação Padrão
df["Data_Ordenacao"] = pd.to_datetime(df["release_date"], errors='coerce')
df["Ordem"] = df["Destaque"].apply(lambda x: 1 if "🔥" in x else 2)
df = df.sort_values(by=["Ordem", "Data_Ordenacao"], ascending=[True, True])
df = df.drop(columns=["Ordem", "Data_Ordenacao"])

# 🔗 Criar hyperlinks clicáveis
df["Link"] = df["game_url"].apply(lambda x: f"{x}" if pd.notna(x) else "Indisponível")

# 📌 Reorganizar colunas
df = df[["Nome", "Data de Lançamento", "Preço", "Gêneros", "Link"]]

# 🔹 Botão "Limpar Filtros"
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Limpar Filtros"):
    st.experimental_rerun()

# ✅ Exibir os lançamentos filtrados
st.markdown("## 🎮 Steam Lançamentos")
st.write(f"🎮 Exibindo **{len(df)}** jogos filtrados")
st.dataframe(df, use_container_width=True)
