from discord import Message

def format_values(valor: float) -> str:
    if valor >= 1_000_000_000:
        return f"{valor / 1_000_000_000:.1f}kkk"
    elif valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f}kk"
    elif valor >= 1_000:
        return f"{valor / 1_000:.1f}k"
    else:
        return f"{valor:.2f}"
    
async def handle_other_commands(message: Message, command: str) -> None:
    await message.channel.send(f"Comando não reconhecido: {command}, tente utilizar o !help para aprender sobre o Bot")