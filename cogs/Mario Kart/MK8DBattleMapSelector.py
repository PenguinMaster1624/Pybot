import discord
from discord.ext import commands
from discord import app_commands
import random

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mk8bm', description = 'Rolls a random Mario Kart 8 Deluxe Battle Mode Map')
  async def mk8bm(self, interaction: discord.Interaction):
    
    lst = ['Dragon Palace', 'Battle Stadium', 'Lunar Colony', 'Wuhu Town', 'Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']

    random.shuffle(lst)
    Selection = random.choice(lst)

    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Battle Mode Map Selector', 
                          description = 'Randomly selects one of the eight maps in Battle Mode', 
                          color = discord.Color.random())
    embed.add_field(name = 'Map Selected!', value = Selection)
    embed.set_footer(text = 'If an unfavorable map, reroll')
    
    await interaction.response.send_message(embed = embed)

async def setup(bot):
  await bot.add_cog(MK8BattleMap(bot))