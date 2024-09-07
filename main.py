from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import webserver
from commands.berry_commands import processar_berry
from commands.craft_commands import calcular_recursos
from commands.help import helper
from utility.utility import handle_other_commands

# Seção de Configuração
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: Final[str] = '!'  # Define o prefixo aqui

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now Running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    if not message.content.startswith(PREFIX):
        return

    command = message.content[len(PREFIX):].strip()
    
    if command.startswith("adicionarBerry"):
        dados_berry = command[len("adicionarBerry"):].strip()
        await processar_berry(message, dados_berry)
    elif command.startswith("calcularRecursos"):
        qtd_berries = command[len("calcularRecursos"):].strip()
        await calcular_recursos(message, qtd_berries)
    elif command.startswith("help"):    
        await helper(message)
    else:
        await handle_other_commands(message)


def main() -> None:
    client.run(TOKEN)
    webserver.keep_alive()

if __name__ == '__main__':
    main()
