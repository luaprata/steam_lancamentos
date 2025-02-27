import streamlit as st
import pandas as pd

# 🚀 Deve ser a PRIMEIRA linha do código!
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# URL do CSV no GitHub (RAW)
CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"

# 🔄 Carregar os dados e atualizar automaticamente a cada 10 minutos
@st.cache_data(ttl=600)  # TTL = 10 minutos
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()

# 🔄 Botão para atualizar os dados manualmente
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()  # Limpa o cache do Streamlit
    st.rerun()  # Atualiza a página corretamente

# Garantir que 'release_date' não tenha valores vazios
df = df.dropna(subset=["release_date"])  # Remove linhas onde 'release_date' é NaT
df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')  # Converte para datetime

# Se o dataframe estiver vazio após remover NaT, definir valores padrão
if df.empty:
    min_date = max_date = pd.to_datetime("today")  # Define a data atual como fallback
else:
    min_date = df["release_date"].min()
    max_date = df["release_date"].max()

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

## 🔹 **Filtro por Gênero**
if "genres" in df.columns:
    generos_exploded = df['genres'].str.split(', ').explode().unique()
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", sorted(generos_exploded))

    if genero_selecionado:
        df = df[df['genres'].apply(lambda x: any(g in x for g in genero_selecionado))]

## 🔹 **Filtro por Data de Lançamento**
data_selecionada = st.sidebar.date_input(
    "Filtrar por data de lançamento:",
    [min_date, max_date] if min_date != max_date else min_date,  # Evita erro com intervalo igual
    min_value=min_date,
    max_value=max_date
)

if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
    df = df[(df["release_date"] >= pd.to_datetime(data_selecionada[0])) & (df["release_date"] <= pd.to_datetime(data_selecionada[1]))]

## 🔹 **Filtro por Preço**
df["price"] = df["price"].astype(str).str.strip()  # Garantir que seja string e limpar espaços
df = df[df["price"] != ""]  # Remover valores vazios

unique_prices = sorted(df["price"].dropna().unique(), key=lambda x: (x.isdigit(), x))

preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", unique_prices)

if preco_selecionado:
    df = df[df["price"].isin(preco_selecionado)]


# Criar links clicáveis na coluna de URL
df["game_url"] = df["game_url"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Acessar</a>')

# Renomear colunas
df = df.rename(columns={
    "title": "Nome",
    "release_date": "Data de Lançamento",
    "price": "Preço",
    "genres": "Gêneros",
    "game_url": "Link"
})

# Reordenar as colunas para deixar o Link por último
df = df[["Nome", "Data de Lançamento", "Preço", "Gêneros", "Link"]]

# Exibir a tabela com os dados filtrados
st.write("### 📋 Lista de Jogos")
st.write("Clique no link para acessar a página do jogo na Steam.")

st.write(
    df.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
