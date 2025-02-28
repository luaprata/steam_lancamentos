# 🔍 Sidebar com filtros
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

## 🔥 **Novo Filtro: Mostrar Apenas Jogos com 🔥**
if st.sidebar.checkbox("🔥 Mostrar apenas lançamentos próximos"):
    df = df[df["Destaque"].str.contains("🔥", na=False)]

# 🔹 **Botão "Limpar Filtros" (Agora no final da sidebar)**
st.sidebar.markdown("---")  # Adiciona uma linha separadora
if st.sidebar.button("🗑️ Limpar Filtros"):
    st.experimental_rerun()
