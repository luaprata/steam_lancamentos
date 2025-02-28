import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 🚀 Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# 🎨 Ajustes Visuais com CSS
st.markdown("""
    <style>
        /* Reduzir a altura da sidebar para expandir a tabela */
        section[data-testid="stSidebar"] {
            min-width: 280px;
            width: 280px;
        }
        
        /* Ajustar margens para expandir tabela */
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

# ✅ Remover colunas duplicadas
df = df.loc[:, ~df.columns.duplicated()].copy()

# ✅ Garantir que todas as colunas estão no formato correto
df["release_date"] = df["release_date"].replace({None: "Indefinido", "nan": "Indefinido", "NaT": "Indefinido"}).astype(str)
df["price"] = df["price"].replace({None: "Indefinido", "nan": "Indefinido", "NaT": "Indefinido"}).astype(str)

# 🔍 Sidebar com filtros (Removemos o título "🔍 Filtros")
## 🔹 **Filtro por Nome**
nome_busca = st.sidebar.text_input("🔎 Buscar jogo por nome:")

if nome_busca:
    df = df[df["title"].str.contains(nome_busca, case=False, na=False)]

## 🔹 **Criar uma cópia de Gêneros para o filtro múltiplo**
if "genres" in df.columns:
    df["Gêneros_Filtro"] = df["genres"].fillna("").astype(str)
    generos_exploded = sorted(set(g for sublist in df["Gêneros_Filtro"].str.split(', ') for g in sublist))
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", generos_exploded)

    if genero_selecionado:
        df = df[df["Gêneros_Filtro"].apply(lambda x: all(g in x for g in genero_selecionado))]

## 🔹 **Filtro por Data de Lançamento**
min_date = pd.to_datetime(df["release_date"], errors='coerce').min()
max_date = pd.to_datetime(df["release_date"], errors='coerce').max()

data_selecionada = st.sidebar.date_input(
    "Filtrar por data de lançamento:",
    [min_date, max_date] if min_date != max_date else min_date,
    min_value=min_date,
    max_value=max_date
)

if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
    df = df[(pd.to_datetime(df["release_date"], errors='coerce') >= pd.to_datetime(data_selecionada[0])) &
            (pd.to_datetime(df["release_date"], errors='coerce') <= pd.to_datetime(data_selecionada[1]))]

## 🔹 **Filtro por Preço**
unique_prices = sorted(df["price"].dropna().unique(), key=lambda x: (x.isdigit(), x))

preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", unique_prices)

if preco_selecionado:
    df = df[df["price"].isin(preco_selecionado)]

## 🔹 **Filtro para Jogos Gratuitos**
if st.sidebar.checkbox("🆓 Mostrar apenas jogos gratuitos"):
    df = df[df["price"].str.lower().str.contains("free", na=False)]

## 🔹 **Filtro para Jogos com Link Disponível**
if st.sidebar.checkbox("🔗 Mostrar apenas jogos com link"):
    df = df[df["game_url"].notna()]

# 🔥 Destaque para Jogos Próximos ao Lançamento (Foguinho)
hoje = datetime.today()
prox_7_dias = hoje + timedelta(days=7)

df["Destaque"] = pd.to_datetime(df["release_date"], errors='coerce').apply(
    lambda x: "🔥 " if pd.notna(x) and x >= hoje and x <= prox_7_dias else "")

df["Nome"] = df["Destaque"] + df["title"]

## 🔥 **Novo Filtro: Mostrar Apenas Jogos com 🔥**
if st.sidebar.checkbox("🔥 Mostrar apenas lançamentos próximos"):
    df = df[df["Destaque"].str.contains("🔥", na=False)]

# 📌 Ordenação Padrão (🔥 primeiro e depois Data de Lançamento)
df["Data_Ordenacao"] = pd.to_datetime(df["release_date"], errors='coerce')
df["Ordem"] = df["Destaque"].apply(lambda x: 1 if "🔥" in x else 2)
df = df.sort_values(by=["Ordem", "Data_Ordenacao"], ascending=[True, True])
df = df.drop(columns=["Ordem", "Data_Ordenacao"])

# 🔗 Criar hyperlinks clicáveis diretamente para `st.dataframe()`
df["Link"] = df["game_url"].apply(lambda x: f"{x}" if pd.notna(x) else "Indisponível")

# 📌 Renomear colunas para exibição final
df = df.rename(columns={
    "release_date": "Data de Lançamento",
    "price": "Preço",
    "genres": "Gêneros"
})

# 📌 Remover a coluna "Gêneros_Filtro" para evitar exibição duplicada
df = df.drop(columns=["Gêneros_Filtro"], errors="ignore")

# 📌 Reordenar colunas
df = df[["Nome", "Data de Lançamento", "Preço", "Gêneros", "Link"]]

# 🔹 **Botão "Limpar Filtros" (Agora no final da sidebar)**
st.sidebar.markdown("---")  # Adiciona uma linha separadora
if st.sidebar.button("🗑️ Limpar Filtros"):
    st.experimental_rerun()

# ✅ **Título Acima da Tabela**
st.markdown("## 🎮 Steam Lançamentos")

# ✅ Exibir contagem de jogos
st.write(f"🎮 Exibindo **{len(df)}** jogos filtrados")

# ✅ Exibir tabela corrigida de forma segura
st.dataframe(df, use_container_width=True)
