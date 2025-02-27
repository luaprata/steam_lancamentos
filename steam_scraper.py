#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

# 🔹 Caminho correto do ChromeDriver
chrome_driver_path = r"C:\Users\User\.wdm\drivers\chromedriver\win64\133.0.6943.141\chromedriver-win32\chromedriver.exe"

# 🔹 Configuração do Selenium
options = Options()
options.add_argument("--headless")  # Roda sem abrir o navegador
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


# 🔹 Função para coletar os jogos sem acessar individualmente
def collect_games():
    print("🔄 Coletando lista de jogos...")
    
    # Iniciar Selenium para buscar os jogos
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Acessar a página da Steam
    URL = "https://store.steampowered.com/search/?filter=popularcomingsoon&ndl=1"
    driver.get(URL)
    time.sleep(3)

    # 🔹 Rolando a página para carregar todos os jogos
    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 0
    while retries < 10:  # Limite para evitar loops infinitos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Espera para carregar mais jogos
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            retries += 1
        else:
            retries = 0
        last_height = new_height

    print("✅ Todos os jogos carregados!")

    # 🔹 Coletando informações básicas dos jogos
    games_data = []
    games = driver.find_elements(By.CSS_SELECTOR, ".search_result_row")  # Seleciona os jogos

    print(f"🔄 Coletando {len(games)} jogos...")

    for game in tqdm(games, desc="📥 Coletando informações dos jogos", unit=" jogo"):
        title_elem = game.find_element(By.CSS_SELECTOR, ".title")
        release_date_elem = game.find_element(By.CSS_SELECTOR, ".search_released")
        
        # 🔹 Captura do preço
        price_elem = game.find_elements(By.CSS_SELECTOR, ".discount_final_price")  # Preço com desconto
        if not price_elem:
            price_elem = game.find_elements(By.CSS_SELECTOR, ".search_price")  # Preço sem desconto
        price = price_elem[0].text.strip() if price_elem else "Indefinido"

        # 🔹 Captura da URL do jogo
        game_url = game.get_attribute("href")

        # 🔹 Captura do título e data de lançamento (fallback para evitar valores vazios)
        title = title_elem.text.strip() if title_elem.text.strip() else "Título não disponível"
        release_date = release_date_elem.text.strip() if release_date_elem.text.strip() else "Data não informada"

        games_data.append({
            "title": title,
            "release_date": release_date,
            "price": price,
            "game_url": game_url,
            "genres": "A capturar..."  # Placeholder para depois capturar os gêneros
        })

    driver.quit()  # Fecha o Selenium
    return games_data


# 🔹 Função para capturar gêneros via Web Scraping (requests + BeautifulSoup)
def get_game_details(game_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(game_url, headers=headers)
        if response.status_code != 200:
            return {"genres": "Erro ao acessar", "title": "Título não disponível", "release_date": "Data não informada"}

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔹 Capturar título e data de lançamento (caso não tenha sido pego antes)
        title_elem = soup.select_one(".apphub_AppName")
        release_date_elem = soup.select_one(".release_date .date")

        title = title_elem.text.strip() if title_elem else "Título não disponível"
        release_date = release_date_elem.text.strip() if release_date_elem else "Data não informada"

        # 🔹 Capturar os gêneros corretamente
        genre_elem = soup.select(".glance_tags.popular_tags a")
        genres = ", ".join([g.text.strip() for g in genre_elem]) if genre_elem else "Sem gênero"

        return {"genres": genres, "title": title, "release_date": release_date}

    except Exception as e:
        return {"genres": f"Erro ao capturar: {str(e)}", "title": "Título não disponível", "release_date": "Data não informada"}


# 🔹 Capturar lista de jogos
games = collect_games()

# 🔹 Capturar gêneros, título e data via BeautifulSoup primeiro
print("🔄 Capturando informações adicionais via Web Scraping...")

for game in tqdm(games, desc="📂 Coletando detalhes dos jogos", unit=" jogo"):
    if game["game_url"] == "URL não disponível":
        game["genres"] = "Sem gênero"
    else:
        details = get_game_details(game["game_url"])
        game["genres"] = details["genres"]
        
        # 🔹 Atualiza título e data de lançamento caso estejam vazios
        if game["title"] == "Título não disponível":
            game["title"] = details["title"]
        if game["release_date"] == "Data não informada":
            game["release_date"] = details["release_date"]

# 🔹 Salvar os dados em CSV
df = pd.DataFrame(games)
df.to_csv("steam_upcoming_games.csv", index=False, encoding="utf-8")

print(f"✅ Coletados {len(games)} jogos futuros e salvos em steam_upcoming_games.csv")


# In[4]:


jupyter nbconvert --to script steam_scraper.ipynb


# In[ ]:




