import discord
from discord import Message, Embed, Color
from datetime import datetime, timedelta
import re
import asyncio
from utility.utility import format_values

BERRYS_RANK_B = [
    'occa', 'pass', 'wacan', 'rindo', 'yache', 'chople', 'kebian', 'shuca', 
    'coba', 'payapa', 'tanga', 'charti', 'kasibb', 'haban', 'roseli', 'colbur', 
    'babiri', 'chilan', 'chesto'
]
BERRYS_RANK_A = ['lum', 'sitrus']

DIFERENCA_HORARIO_BRASILIA = -3  # Ajuste para UTC-3

async def processar_berry(message: Message, dados_berry: str) -> None:
    berry_data = extrair_dados_berry(dados_berry)
    if not berry_data:
        await message.channel.send("Siga o modelo certo, caboco. !help, caso tenha dúvida")
        return

    nome_berry, quantia, horario_plantacao, valor_berry = berry_data

    try:
        valor_total, horario_colheita_final = calcular_valores(nome_berry, quantia, valor_berry, horario_plantacao)
        dia_colheita = formatar_dia_colheita(horario_colheita_final)
        horario_apodrecimento = apodrecimento_da_colheita(horario_colheita_final)

        embed = criar_embed_colheita(nome_berry, quantia, valor_total, dia_colheita)
        await message.channel.send(embed=embed)

        await agendar_notificacao_colheita(message, nome_berry, horario_colheita_final, int(quantia), valor_berry, horario_apodrecimento)

    except ValueError:
        await message.channel.send('Vish, alguma coisa deu merda!')

def extrair_dados_berry(dados_berry: str):
    pattern = r"Nome da Berry:\s*(.*?)\s*Quantia:\s*(.*?)\s*Horário da plantação:\s*(.*?)\s*Valor da Berry:\s*(.*)"
    match = re.search(pattern, dados_berry, re.DOTALL)

    if match:
        nome_berry = match.group(1).strip()
        quantia = match.group(2).strip()
        horario_plantacao = match.group(3).strip()
        valor_berry = match.group(4).strip()
        return nome_berry, quantia, horario_plantacao, valor_berry
    return None

def calcular_valores(nome_berry: str, quantia: str, valor_berry: str, horario_plantacao: str):
    quantia = int(quantia)
    valor_berry = float(valor_berry)
    valor_total = format_values(quantia * valor_berry)

    hoje = datetime.utcnow()  # Obtém a data e hora atual em UTC
    hoje_br = hoje + timedelta(hours=DIFERENCA_HORARIO_BRASILIA)  # Ajusta para o horário de Brasília

    horario_plantacao_formatado = datetime.strptime(horario_plantacao, '%H:%M').replace(year=hoje_br.year, month=hoje_br.month, day=hoje_br.day)
    horario_plantacao_formatado = horario_plantacao_formatado - timedelta(hours=DIFERENCA_HORARIO_BRASILIA)  # Ajusta o horário da plantação para UTC

    if nome_berry in BERRYS_RANK_A:
        horario_colheita = timedelta(hours=8)
    elif nome_berry in BERRYS_RANK_B:
        horario_colheita = timedelta(hours=6)
    else:
        raise ValueError("Mermão, digite o nome da berry certo!")

    horario_colheita_final = horario_plantacao_formatado + horario_colheita
    horario_colheita_final_br = horario_colheita_final + timedelta(hours=DIFERENCA_HORARIO_BRASILIA)  # Ajusta o horário de colheita para o horário de Brasília
    return valor_total, horario_colheita_final_br

def formatar_dia_colheita(horario_colheita_final: datetime):
    return horario_colheita_final.strftime("%d/%m/%Y às [**%H:%M**]")

def apodrecimento_da_colheita(horario_colheita_final: datetime) -> str:
    horario_apodrecimento = horario_colheita_final + timedelta(hours=30)
    return horario_apodrecimento.strftime("%d/%m/%Y às [**%H:%M**]")

def criar_embed_colheita(nome_berry: str, quantia: int, valor_total: str, dia_colheita: str) -> Embed:
    berry_image_url = f"https://www.serebii.net/itemdex/sprites/{nome_berry}berry.png"
    embed = Embed(
        title="Colheita adicionada",
        description=(
            f"**Nome:** {nome_berry}\n" 
            f"**Quantia:** {quantia}\n"
            f"**Retorno Da Colheita:** **{valor_total}**\n"
            f"**Dia da Colheita:** {dia_colheita}"
        ),
        color=Color.green()
    )
    embed.set_author(name=f'{nome_berry} Berry', icon_url=berry_image_url)
    return embed

async def agendar_notificacao_colheita(message: Message, nome_berry: str, horario_colheita_final: datetime, quantia: int, valor_berry: str, horario_apodrecimento: datetime) -> None:
    berry_image_url = f"https://www.serebii.net/itemdex/sprites/{nome_berry}berry.png"
    valor_berry = float(valor_berry)
    agora = datetime.utcnow()  # Obtém a data e hora atual em UTC
    agora_br = agora + timedelta(hours=DIFERENCA_HORARIO_BRASILIA)  # Ajusta para o horário de Brasília

    tempo_ate_colheita = (horario_colheita_final - agora).total_seconds()

    await asyncio.sleep(tempo_ate_colheita)

    quantia = int(quantia)

    lucro_formatado = format_values(quantia * valor_berry)
    lucro_maximo_formatado = format_values((quantia * 2) * valor_berry)
    media = (quantia * 2) / quantia 

    embed = Embed(
        title=f"⏰ Colheita {horario_colheita_final}: ",
        description=(
            f"# ✅ Suas {nome_berry} estão prontas !!\n"
            "\n"
            "\n"
            f"**Quantidade Pronta para Colher:** {quantia}\n"
            "\n"
            f"**Lucro Esperado:** 💸 {lucro_formatado}\n"
            "\n"
            f"**Quantidade Mínima de berries:** {quantia}\n"
            "\n"
            f"**Lucro Máximo:** 💸 {lucro_maximo_formatado}\n"
            "\n"
            f"**Quantidade Máxima de berries:** {quantia * 2}\n"
            "\n"
            f"**Média de Berries dessa Colheita:** {media}\n"
            f"# ❗❗ A colheita apodrecerá às {horario_apodrecimento} "
        ),
        color=Color.blue()
    )

    embed.set_author(name=f'{nome_berry} Berry', icon_url=berry_image_url)

    try:
        await message.author.send(embed=embed)
    except discord.Forbidden:
        await message.channel.send(f"Não foi possível enviar uma mensagem privada para {message.author.name}.")
