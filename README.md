# 🚀 Steam Upcoming Games Scraper

Este projeto realiza web scraping na Steam para coletar informações sobre os jogos que serão lançados em breve. Ele extrai dados como título, data de lançamento, preço e gêneros dos jogos.

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

---

## ⚙️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Baixe e configure o ChromeDriver:**
   - Faça o download do [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Certifique-se de que a versão corresponde ao seu Google Chrome.
   - Atualize o caminho do ChromeDriver no código se necessário.

---

## ▶️ Como Executar o Script

1. **Execute o script de scraping:**
   ```bash
   python steam_scraper.py
   ```

2. **Os dados coletados serão salvos em um arquivo CSV:**
   ```bash
   steam_upcoming_games.csv
   ```

---

## 📂 Estrutura do Projeto
```
📦 steam_scraper
├── 📜 steam_scraper.py      # Script principal de scraping
├── 📜 requirements.txt      # Lista de dependências
├── 📜 README.md             # Documentação do projeto
├── 📜 steam_upcoming_games.csv  # Dados extraídos
```

---

## 💡 Melhorias Futuras
- Implementar **API** para consulta dos jogos coletados.
- Criar um **dashboard** para visualizar os dados.
- Melhorar a **performance** na extração de dados.

---

## 🤝 Contribuição
Sinta-se à vontade para contribuir! Para isso:

1. Faça um **fork** do repositório.
2. Crie uma **branch** para sua funcionalidade.
3. Faça um **commit** com suas alterações.
4. Abra um **pull request**.

---

## 📜 Licença
Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido por [Seu Nome](https://github.com/seu-usuario) 🚀

