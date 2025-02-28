import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 🚀 Configuração da Página
st.set_page_config(page_title="🎮 Steam Lançamentos", layout="wide")

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
df = df.loc[:, ~df.columns.duplicated()]

# ✅ Garantir que todas as colunas estão no formato correto
df = df.astype(str)

# ✅ Remover valores inválidos
df = df.dropna(how="any")  
df = df.replace({None: "", "nan": "", "NaT": ""})

# ✅ Converter 'release_date' para datetime
df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')

# Se o dataframe estiver vazio após remover NaT, definir valores padrão
if df.empty:
    min_date = max_date = pd.to_datetime("today")
else:
    min_date = df["release_date"].min()
    max_date = df["release_date"].max()

# 🔍 Sidebar com filtros
st.sidebar.header("🔍 Filtros")

## 🔹 **Filtro por Nome**
nome_busca = st.sidebar.text_input("🔎 Buscar jogo por nome:")

if nome_busca:
    df = df[df["title"].str.contains(nome_busca, case=False, na=False)]

## 🔹 **Filtro por Gênero**
if "genres" in df.columns:
    df["Gêneros"] = df["genres"].fillna("").astype(str)
    generos_exploded = sorted(set(g for sublist in df["Gêneros"].str.split(', ') for g in sublist))
    genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", generos_exploded)

    if genero_selecionado:
        df = df[df["Gêneros"].apply(lambda x: all(g in x for g in genero_selecionado))]

## 🔹 **Filtro por Data de Lançamento**
data_selecionada = st.sidebar.date_input(
    "Filtrar por data de lançamento:",
    [min_date, max_date] if min_date != max_date else min_date,
    min_value=min_date,
    max_value=max_date
)

if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
    df = df[(df["release_date"] >= pd.to_datetime(data_selecionada[0])) & (df["release_date"] <= pd.to_datetime(data_selecionada[1]))]

## 🔹 **Filtro por Preço**
df["price"] = df["price"].astype(str).str.strip()
df = df[df["price"] != ""]

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

## 🔹 **Ordenar por**
opcoes_ordenacao = ["Nome", "Data de Lançamento", "Preço"]
ordem_selecionada = st.sidebar.selectbox("📊 Ordenar por:", opcoes_ordenacao)

# Aplicando ordenação
if ordem_selecionada == "Nome":
    df = df.sort_values(by="title", ascending=True)
elif ordem_selecionada == "Data de Lançamento":
    df = df.sort_values(by="release_date", ascending=True)
elif ordem_selecionada == "Preço":
    df = df.sort_values(by="price", ascending=True)

## 🔹 **Botão "Limpar Filtros"**
if st.sidebar.button("🗑️ Limpar Filtros"):
    st.experimental_rerun()

# 🔥 Destaque para Jogos Próximos ao Lançamento
hoje = datetime.today()
prox_7_dias = hoje + timedelta(days=7)

df["Destaque"] = df["release_date"].apply(lambda x: "🔥 " if x >= hoje and x <= prox_7_dias else "")

df["Nome"] = df["Destaque"] + df["title"]
df = df.drop(columns=["Destaque"])

# 🔗 Exibir links como texto puro (removendo HTML para evitar erro)
df["Link"] = df["game_url"]

# 📌 Renomear colunas
df = df.rename(columns={
    "release_date": "Data de Lançamento",
    "price": "Preço",
    "genres": "Gêneros"
})

# 📌 Reordenar colunas
df = df[["Nome", "Data de Lançamento", "Preço", "Gêneros", "Link"]]

# ✅ Verificar tipos antes de exibir
st.write("🔍 Verificando tipos de dados antes de exibir:")
st.write(df.dtypes)

# ✅ Exibir contagem de jogos
st.write(f"🎮 Exibindo **{len(df)}** jogos filtrados")

# ✅ Exibir tabela corrigida
st.dataframe(df, use_container_width=True)
