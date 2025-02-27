import streamlit as st
import pandas as pd

# URL do CSV no GitHub (RAW)
CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)

    # Converter colunas para tipos apropriados
    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')  # Converter para data
    df["price"] = df["price"].astype(str)  # Manter preço como string
    
    return df

df = load_data()

# Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# Título da Aplicação
st.title("🎮 Próximos Lançamentos na Steam")

st.write("Este aplicativo exibe os próximos jogos a serem lançados na Steam com base nos dados coletados via Web Scraping.")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

## 🔹 **1️⃣ Filtro por Gênero (Quebrando corretamente os gêneros)**
if "genres" in df.columns:
    generos_exploded = df['genres'].str.split(', ').explode().unique()  # Quebra os gêneros
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", sorted(generos_exploded))

    if genero_selecionado:
        df = df[df['genres'].apply(lambda x: any(g in x for g in genero_selecionado))]

## 🔹 **2️⃣ Filtro por Data de Lançamento**
if "release_date" in df.columns:
    min_date = df["release_date"].min()
    max_date = df["release_date"].max()

    data_selecionada = st.sidebar.date_input("Filtrar por data de lançamento:", [min_date, max_date], min_value=min_date, max_value=max_date)

    if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
        df = df[(df["release_date"] >= pd.to_datetime(data_selecionada[0])) & (df["release_date"] <= pd.to_datetime(data_selecionada[1]))]

## 🔹 **3️⃣ Filtro por Preço**
if "price" in df.columns:
    unique_prices = df["price"].unique()
    preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", sorted(unique_prices))

    if preco_selecionado:
        df = df[df["price"].isin(preco_selecionado)]

# Criar links clicáveis na coluna de URL
df["game_url"] = df["game_url"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Acessar</a>')

# Exibir a tabela com os dados filtrados
st.write("### 📋 Lista de Jogos")
st.write("Clique no link para acessar a página do jogo na Steam.")

st.write(
    df[["title", "release_date", "price", "game_url", "genres"]].to_html(escape=False, index=False),
    unsafe_allow_html=True
)
