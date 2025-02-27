import streamlit as st
import pandas as pd

# URL do CSV no GitHub (RAW)
CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)

    # Converter colunas para tipos apropriados
    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')  # Corrige datas inválidas
    df["price"] = df["price"].astype(str)  # Mantém o preço como string (caso tenha variações)
    
    return df

df = load_data()

# Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# Título da Aplicação
st.title("🎮 Próximos Lançamentos na Steam")

st.write("Este aplicativo exibe os próximos jogos a serem lançados na Steam com base nos dados coletados via Web Scraping.")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# Filtro por gênero
if "genres" in df.columns:
    generos = df['genres'].str.split(', ').explode().unique()
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", generos)

    if genero_selecionado:
        df = df[df['genres'].apply(lambda x: any(g in x for g in genero_selecionado))]

# Filtro por preço (opcional, se os preços forem numéricos)
if "price" in df.columns:
    unique_prices = df["price"].unique()
    preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", unique_prices)

    if preco_selecionado:
        df = df[df["price"].isin(preco_selecionado)]

# Exibir os dados filtrados
st.dataframe(df)

# Criar link clicável para cada jogo
st.write("### 🔗 Acesse os jogos na Steam")
df["game_url"] = df["game_url"].apply(lambda x: f"[Link]( {x} )")

st.dataframe(df[["title", "release_date", "price", "game_url", "genres"]], unsafe_allow_html=True)
