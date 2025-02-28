import discord
from discord.ext import commands, tasks
import pandas as pd
import requests
import os
from datetime import datetime, timedelta

# 🔹 Configuração do bot (usando commands.Bot para suporte a comandos)
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if TOKEN is None:
    raise ValueError("❌ ERRO: A variável TOKEN não está definida! Verifique no Railway.")
if CHANNEL_ID is None:
    raise ValueError("❌ ERRO: A variável CHANNEL_ID não está definida! Verifique no Railway.")

CHANNEL_ID = int(CHANNEL_ID.strip())

# Criar instância do bot com o prefixo "!"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔹 URL do CSV com os lançamentos
CSV_URL = "https://raw.githubusercontent.com/luaprata/steam_lancamentos/main/steam_upcoming_games.csv"

# 🔹 Função para buscar os lançamentos recentes (🔥)
def get_upcoming_games():
    try:
        df = pd.read_csv(CSV_URL)

        # Garantir que release_date esteja no formato datetime
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
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    send_daily_updates.start()  # Iniciar a tarefa de envio automático

# 🔹 Função para enviar a notificação no Discord
async def send_game_updates(channel):
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

# 🔹 Criar um comando `!lançamentos` para exibir os jogos sob demanda
@bot.command(name="lançamentos")
async def lancamentos(ctx):
    await ctx.send("🔍 Buscando os lançamentos mais próximos...")
    await send_game_updates(ctx.channel)

# 🔹 Tarefa automática diária para enviar os lançamentos automaticamente
@tasks.loop(hours=24)
async def send_daily_updates():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await send_game_updates(channel)
    else:
        print("❌ ERRO: Canal não encontrado!")

# 🔹 Iniciar o bot
bot.run(TOKEN)
