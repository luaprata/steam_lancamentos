import discord
import pandas as pd
import requests
import asyncio
import os
from datetime import datetime, timedelta

# 🔹 Pegando as variáveis de ambiente do Railway (ou manualmente para testes locais)
TOKEN = os.getenv("TOKEN")  # 🔑 Token do bot do Discord
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # 📢 ID do canal onde o bot enviará as mensagens

# 🔹 URL do CSV com os lançamentos
CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"

# 🔹 Configuração do bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Testar se as variáveis de ambiente estão carregando
print(f"TOKEN: {os.getenv('TOKEN')}")
print(f"CHANNEL_ID: {os.getenv('CHANNEL_ID')}")  # Isso deve imprimir o ID do canal correto

# 🔹 Função para buscar os lançamentos próximos (🔥)
def get_upcoming_games():
    try:
        df = pd.read_csv(CSV_URL)

        # Garantir que release_date está em formato datetime
        df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')

        # Definir a janela de lançamentos próximos (até 7 dias)
        hoje = datetime.today()
        prox_7_dias = hoje + timedelta(days=7)

        # Filtrar apenas jogos que serão lançados nos próximos 7 dias
        df = df[(df["release_date"] >= hoje) & (df["release_date"] <= prox_7_dias)]

        # Adicionar 🔥 ao nome dos jogos
        df["Nome"] = "🔥 " + df["title"]

        # Retornar os jogos ordenados por data de lançamento
        return df.sort_values(by="release_date")

    except Exception as e:
        print(f"❌ Erro ao buscar os jogos: {e}")
        return pd.DataFrame()  # Retorna uma tabela vazia se houver erro

# 🔹 Evento: Quando o bot estiver pronto
@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')
    
    # Aguarde 5 segundos antes de enviar a primeira notificação
    await asyncio.sleep(5)

    # 🔄 Rodar a função de notificação automaticamente todo dia
    while True:
        await send_game_updates()
        await asyncio.sleep(86400)  # Espera 24h para a próxima atualização

# 🔹 Função para enviar a notificação no Discord
async def send_game_updates():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Canal não encontrado!")
        return

    games = get_upcoming_games()

    if games.empty:
        await channel.send("🚫 Nenhum jogo novo próximo do lançamento!")
        return
    
    # 🔹 Criar Embed no Discord
    embed = discord.Embed(title="🔥 Jogos Lançando em Breve!", color=0xffa500)
    
    # 🔹 Limitar a 10 jogos por mensagem para evitar flood
    max_games = 10
    for _, row in games.head(max_games).iterrows():
        embed.add_field(
            name=row["Nome"],
            value=f"📅 {row['release_date'].strftime('%d %b, %Y')} | [🔗 Acessar]({row['game_url']})",
            inline=False
        )

    # 🔹 Enviar a mensagem no canal
    await channel.send(embed=embed)

    # 🔹 Se houver mais jogos, enviar um link para consultar todos
    if len(games) > max_games:
        await channel.send(f"📌 Existem **{len(games) - max_games}** jogos a mais. Veja a lista completa no [Steam Lançamentos](https://seu-link.com).")

# 🔹 Iniciar o bot
client.run(TOKEN)
