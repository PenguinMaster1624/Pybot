from discord.ext import commands
from discord import app_commands
import random, discord, sqlite3

class MK8Map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def db_connect(self, command: str, cup: tuple[str | None]) -> list[tuple[str]]:
    with sqlite3.connect('Utils/Game Stuff.db') as db:
      cursor = db.cursor()
      if all(cup):
        return [course for course in cursor.execute(command, cup)]

      else:
        return [course for course in cursor.execute(command)]


  @app_commands.command(name = 'mk8m', description = 'Rolls a random map from the available Mario Kart 8 Deluxe maps, includes DLC')
  async def mk8m(self, interaction: discord.Interaction, cup: str = None):

    if cup is not None:
      cup = cup.title().strip()
      if cup in ['Mushroom', 'Flower', 'Star', 'Special', 'Shell', 'Banana', 'Leaf', 'Lightning', 'Egg', 'Crossing', 'Triforce', 'Bell', 'Golden Dash', 'Lucky Cat', 'Turnip', 'Propeller', 'Rock', 'Moon', 'Fruit', 'Boomerang', 'Feather', 'Cherry', 'Acorn', 'Spiny']:
        command = 'SELECT Course, Cup FROM "MK8DX Race Courses" WHERE Cup = ?'

      else:
        await interaction.response.send_message(f'{cup} is not a valid weapon class', ephemeral = True)
    
    else:
      command = 'SELECT Course, Cup FROM "MK8DX Race Courses"'

    courses = await self.db_connect(command = command, cup = (cup,))
    course = random.choice(courses)

    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Map Selector', color = discord.Color.random())
    embed.add_field(name = 'The Council Has Decided!', value = course[0])
    embed.set_footer(text = f'Found in the {course[1]} Cup')
    await interaction.response.send_message(embed = embed, ephemeral = True)


  @mk8m.autocomplete('cup')
  async def mk8m_autocomplete(self, interaction: discord.Interaction, current: str)-> list[app_commands.Choice[str]]:
    cups = ['Mushroom', 'Flower', 'Star', 'Special', 'Shell', 'Banana', 'Leaf', 'Lightning', 'Egg', 'Crossing', 'Triforce', 'Bell', 'Golden Dash', 'Lucky Cat', 'Turnip', 'Propeller', 'Rock', 'Moon', 'Fruit', 'Boomerang', 'Feather', 'Cherry', 'Acorn', 'Spiny']
    return [app_commands.Choice(name = cup, value = cup) for cup in cups if current.lower() in cup.lower()]

async def setup(bot: commands.Bot):
  await bot.add_cog(MK8Map(bot))