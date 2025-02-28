import os

# Testar se as variáveis de ambiente estão carregando corretamente
print(f"TOKEN: {os.getenv('TOKEN')}")
print(f"CHANNEL_ID: {os.getenv('CHANNEL_ID')}")  # Isso deve imprimir o ID do canal correto

CHANNEL_ID = os.getenv("CHANNEL_ID")

if CHANNEL_ID is None or CHANNEL_ID.strip() == "":
    raise ValueError("❌ ERRO: A variável CHANNEL_ID não está definida! Verifique no Railway.")

CHANNEL_ID = int(CHANNEL_ID.strip())  # Converter após garantir que não está vazia
