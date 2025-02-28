import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# 📊 Carregar Dados
@st.cache_data(ttl=600)
def load_data():
    CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"
    return pd.read_csv(CSV_URL)

df = load_data()

df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
df = df.dropna(subset=["release_date"])

df["price"] = df["price"].astype(str)
df["is_free"] = df["price"].str.contains("free", case=False, na=False)

generos_series = df["genres"].dropna().str.split(", ").explode()
generos_contagem = generos_series.value_counts()

# 🔍 Sidebar com filtros
st.sidebar.title("🔍 Filtros")
nome_busca = st.sidebar.text_input("Buscar jogo por nome:")
if nome_busca:
    df = df[df["title"].str.contains(nome_busca, case=False, na=False)]

generos_exploded = sorted(set(g for sublist in df["genres"].dropna().str.split(', ') for g in sublist))
genero_selecionado = st.sidebar.multiselect("Filtrar por gênero:", generos_exploded)
if genero_selecionado:
    df = df[df["genres"].apply(lambda x: any(g in str(x) for g in genero_selecionado))]

min_date = df["release_date"].min()
max_date = df["release_date"].max()
data_selecionada = st.sidebar.date_input("Filtrar por data de lançamento:", [min_date, max_date], min_value=min_date, max_value=max_date)
if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
    df = df[(df["release_date"] >= data_selecionada[0]) & (df["release_date"] <= data_selecionada[1])]

if st.sidebar.checkbox("🆓 Mostrar apenas jogos gratuitos"):
    df = df[df["is_free"]]
if st.sidebar.checkbox("🔥 Mostrar apenas lançamentos próximos"):
    hoje = datetime.today()
    prox_7_dias = hoje + timedelta(days=7)
    df = df[(df["release_date"] >= hoje) & (df["release_date"] <= prox_7_dias)]

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Limpar Filtros"):
    st.experimental_rerun()

# 📌 Layout principal dividido
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🎮 Steam Lançamentos")
    st.write(f"🎮 Exibindo **{len(df)}** jogos filtrados")
    st.dataframe(df, use_container_width=True)

with col2:
    st.markdown("## 📊 Analytics")
    st.subheader("🎮 Top 10 Gêneros Mais Frequentes")
    fig, ax = plt.subplots(figsize=(8, 4))
    generos_contagem.head(10).plot(kind="barh", ax=ax, color="royalblue")
    ax.set_xlabel("Quantidade de Jogos")
    ax.set_ylabel("Gênero")
    ax.set_title("Top 10 Gêneros de Jogos")
    ax.invert_yaxis()
    st.pyplot(fig)
    
    st.subheader("💰 Proporção de Jogos Gratuitos vs Pagos")
    fig, ax = plt.subplots(figsize=(5, 5))
    free_paid_counts = df["is_free"].value_counts()
    ax.pie(free_paid_counts, labels=["Pagos", "Gratuitos"], autopct="%1.1f%%", startangle=90, colors=["tomato", "gold"])
    ax.set_title("Proporção de Jogos Gratuitos vs Pagos")
    st.pyplot(fig)
    
    st.subheader("🔥 Jogos a serem lançados na próxima semana")
    hoje = datetime.today()
    prox_7_dias = hoje + timedelta(days=7)
    upcoming_count = df[(df["release_date"] >= hoje) & (df["release_date"] <= prox_7_dias)].shape[0]
    
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.bar(["Lançamentos Próximos"], [upcoming_count], color="orange")
    ax.set_ylabel("Quantidade de Jogos")
    ax.set_title("Jogos que serão lançados na próxima semana")
    st.pyplot(fig)
