# 🚀 Lançamentos Steam

Este projeto realiza **web scraping** na Steam para coletar informações sobre os jogos que serão lançados em breve. O pipeline inclui **extração de dados**, **atualização automática no GitHub**, **visualização no Streamlit** e **notificações via bot no Discord**.

🔗 **[Acesse a Interface Web no Streamlit](https://luaprata-steamlancamentos.streamlit.app/)**  
🤖 **Bot no Discord envia notificações diárias sobre lançamentos!**

---

## 📌 Fluxo Completo do Projeto
> **1️⃣ Web Scraper** → **2️⃣ GitHub Actions** → **3️⃣ Geração CSV** → **4️⃣ Streamlit (Interface Web)** → **5️⃣ Bot do Discord via Railway** → **6️⃣ Notificações Automáticas**

### 🔄 Como Funciona o Processo
1. **Coleta de Dados da Steam**:  
   - O **web scraper** usa **Selenium** e **BeautifulSoup** para extrair informações da Steam.
   - Captura **título, data de lançamento, preço, gêneros e link do jogo**.
   - Filtra jogos com **restrição de idade**.

2. **Atualização Automática via GitHub Actions**:  
   - O script roda **periodicamente** (exemplo: a cada 12h).  
   - O **CSV atualizado** é enviado para o repositório do GitHub.  

3. **Interface Web com Streamlit**:  
   - Exibe a **lista de lançamentos** diretamente da Steam.  
   - Permite **filtragem por data, gênero e preço**.
   - Tabela com **links diretos para a Steam**.

4. **Bot no Discord via Railway**:  
   - O bot no Discord lê o CSV atualizado e envia **notificações diárias**.  
   - Comando `!lançamentos` permite ver os jogos lançando em breve **sob demanda**.  
   - Deploy automático no **Railway**, funcionando **24/7**.

---

## 🕹️ Estrutura do Projeto
```
📺 steam_scraper
├── 📝 steam_scraper.py          # Script de scraping (extrai dados da Steam)
├── 📝 requirements.txt          # Dependências do projeto
├── 📝 README.md                 # Documentação do projeto
├── 📝 steam_upcoming_games.csv  # Dados coletados dos jogos
├── 📝 app.py                    # Interface web (Streamlit)
├── 📝 bot.py                    # Bot do Discord para notificações
├── 📝 Procfile                  # Arquivo para deploy no Railway
├── 📝 .github/workflows/update_csv.yml  # Automação no GitHub Actions
```

---

## 🚀 Tecnologias Utilizadas
🔹 **Python 3.8+**  
🔹 **Selenium** (para navegação automatizada na Steam)  
🔹 **BeautifulSoup** (para extração de dados das páginas)  
🔹 **Pandas** (para manipulação e exportação de dados)  
🔹 **Tqdm** (barra de progresso durante a raspagem)  
🔹 **Streamlit** (interface web interativa)  
🔹 **Discord.py** (bot do Discord para notificações)  
🔹 **Railway** (deploy do bot do Discord)  
🔹 **GitHub Actions** (atualização automática do CSV)  

---

## 🔧 Como Rodar o Projeto Localmente
### 1️⃣ Clonar o Repositório
```sh
git clone https://github.com/seu-usuario/steam_scraper.git
cd steam_scraper
```

### 2️⃣ Instalar Dependências
```sh
pip install -r requirements.txt
```

### 3️⃣ Rodar o Scraper
```sh
python steam_scraper.py
```
Isso irá gerar o arquivo **`steam_upcoming_games.csv`**.

### 4️⃣ Rodar a Interface Web (Streamlit)
```sh
streamlit run app.py
```
Acesse a interface pelo navegador.

### 5️⃣ Rodar o Bot do Discord
```sh
python bot.py
```
🔔 O bot irá **enviar as notificações automaticamente** e também responder ao comando `!lançamentos`.

---

## 💡 Melhorias Futuras
👉 **API para consulta dos jogos coletados**  
👉 **Dashboard interativo com gráficos**  
👉 **Personalização do bot (notificações por usuário, comandos extras)**  
👉 **Suporte a mais lojas além da Steam (Epic, GOG, etc.)**  

---

### 👨‍💻 Desenvolvido por [Luã Prata](https://github.com/luaprata) 🚀  
Se gostou do projeto, **deixe uma ⭐ no repositório** e contribua com sugestões! 😃  
```
