from discord import Message, Embed, Color

async def helper (message: Message):
    embed = Embed(
        title="Instruções do Bot",
            description=(
                "## !adicionarberry \n"
                "Modelo a seguir: \n"
                "Nome da Berry: \n"
                "Quantia Plantada: \n"
                "Horário da plantação:\n"
                "Valor da Berry: \n"

                "## Exemplo Pronto ## \n"
                "!adicionarBerry \n"
                "Nome da Berry: lum\n"
                "Quantia: 10\n"
                "Horário da plantação: 13:58\n"
                "Valor da Berry: 25000\n"

                "## !calcularRecursos \n"
                "Nesse comando, só basta digitar o número após o comando\n"
                "Exemplo: !calcularRecursos 20"
        
        ),
        color=Color.blue()
    )
    await message.channel.send(embed=embed)