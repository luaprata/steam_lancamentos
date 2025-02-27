# 🚀 Lançamentos Steam

Este projeto realiza web scraping na Steam para coletar informações sobre os jogos que serão lançados em breve. Ele extrai dados como título, data de lançamento, preço e gêneros dos jogos.

**URL Streamlit:**  https://luaprata.streamlit.app/

---

## 📌 Funcionalidades
- **Coleta de jogos futuros** listados na Steam.
- **Raspagem de dados** via Selenium e BeautifulSoup.
- **Tratamento de restrições de idade** para jogos com bloqueio.
- **Geração de um arquivo CSV** contendo todas as informações coletadas.

---

## 🛠️ Tecnologias Utilizadas

- **Python** (3.8+)
- **Selenium** (para navegar e interagir com a Steam)
- **BeautifulSoup** (para extração de informações da página)
- **Pandas** (para manipulação e exportação de dados)
- **Tqdm** (para barra de progresso)
- **Streamlit** (para interface web)

---

## 📂 Estrutura do Projeto
```
📦 steam_scraper
├── 📜 steam_scraper.py          # Script principal de scraping
├── 📜 requirements.txt          # Lista de dependências
├── 📜 README.md                 # Documentação do projeto
├── 📜 steam_upcoming_games.csv  # Dados extraídos
├── 📜 app.py                    # Script streamlit

```

---

## 💡 Melhorias Futuras
- Implementar **API** para consulta dos jogos coletados.
- Criar um **dashboard** para visualizar os dados.
- Melhorar a **performance** na extração de dados.

---


Desenvolvido por [Luã Prata](https://github.com/luaprata) 🚀

