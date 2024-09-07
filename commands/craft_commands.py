
from discord import Color, Embed, Message


IMAGEM_MAJOR_SEED_BAG = "https://wiki.pokexgames.com/images/d/d4/Major_Seed_Bag.png"
IMAGEM_MINOR_SEED_BAG = "https://wiki.pokexgames.com/images/2/25/Minor_Seed_Bag.png"
IMAGEM_SEEDS = "https://wiki.pokexgames.com/images/2/2e/Seed.png"
IMAGEM_LEAVES = "https://wiki.pokexgames.com/images/f/f1/Leaves.png"
IMAGEM_BAG_OF_POLLENS = "https://wiki.pokexgames.com/images/b/bc/BagOfPollem.png"

# Recursos necessários para o craft
recursos_por_minor_seed_bag = {
    'seeds': 200,
    'leaves': 25,
    'bag_of_pollens': 20
}

minor_seed_bag_por_major = 10
major_seed_bag_por_berry = 1


def calcular_recursos_necessarios(qtd_berry: int) -> dict:
    total_major_seed_bags = qtd_berry * major_seed_bag_por_berry
    total_minor_seed_bags = total_major_seed_bags * minor_seed_bag_por_major
    
    total_seeds = total_minor_seed_bags * recursos_por_minor_seed_bag['seeds']
    total_leaves = total_major_seed_bags * recursos_por_minor_seed_bag['leaves']
    total_bag_of_pollens = total_major_seed_bags * recursos_por_minor_seed_bag['bag_of_pollens']

    return {
        'berries': qtd_berry,
        'major_seed_bag': total_major_seed_bags,
        'minor_seed_bag': total_minor_seed_bags,
        'seeds': total_seeds,
        'leaves': total_leaves,
        'bag_of_pollens': total_bag_of_pollens
    }

async def calcular_recursos(message: Message, qtd_berries: str) -> None:
    try:
        qtd_berries = int(qtd_berries)
        recursos = calcular_recursos_necessarios(qtd_berries)
        
        embed = Embed(
            title="Recursos Necessários",
            description=(
                f"Para criar **{recursos['berries']}** berries, você precisa de:\n"
                "\n"
                f"✨  {recursos['major_seed_bag']} major seed bags\n"
                "\n" 
                f"✨  {recursos['minor_seed_bag']} minor seed bags\n"
                "\n" 
                f"🌱  {recursos['seeds']} seeds\n"
                "\n" 
                f"🍃  {recursos['leaves']} leaves\n"
                "\n" 
                f"🐝  {recursos['bag_of_pollens']} bag of pollens"
            ),
            color=Color.green()
        )

        await message.channel.send(embed=embed)
        
    except ValueError:
        await message.channel.send("E aí, pô. Coloque um número de berry ai.")