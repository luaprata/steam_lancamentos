import streamlit as st
import pandas as pd

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
    st.experimental_rerun()  # Recarrega a página

# Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

# Título da Aplicação
st.title("🎮 Próximos Lançamentos na Steam")

st.write("Este aplicativo exibe os próximos jogos a serem lançados na Steam com base nos dados coletados via Web Scraping.")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

## 🔹 **Filtro por Gênero**
if "genres" in df.columns:
    generos_exploded = df['genres'].str.split(', ').explode().unique()
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", sorted(generos_exploded))

    if genero_selecionado:
        df = df[df['genres'].apply(lambda x: any(g in x for g in genero_selecionado))]

## 🔹 **Filtro por Data de Lançamento**
if "release_date" in df.columns:
    min_date = df["release_date"].min()
    max_date = df["release_date"].max()

    data_selecionada = st.sidebar.date_input("Filtrar por data de lançamento:", [min_date, max_date], min_value=min_date, max_value=max_date)

    if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
        df = df[(df["release_date"] >= pd.to_datetime(data_selecionada[0])) & (df["release_date"] <= pd.to_datetime(data_selecionada[1]))]

## 🔹 **Filtro por Preço**
if "price" in df.columns:
    unique_prices = df["price"].unique()
    preco_selecionado = st.sidebar.multiselect("Filtrar por preço:", sorted(unique_prices))

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
