from discord.ext import commands
from discord import app_commands
import random, discord

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.stages = ['Dragon Palace', 'Battle Stadium', 'Lunar Colony', 'Wuhu Town', 'Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']

  @app_commands.command(name = 'mk8bm', description = 'Rolls a random Mario Kart 8 Deluxe Battle Mode Map')
  async def mk8bm(self, interaction: discord.Interaction):
  
    random.shuffle(self.stages)
    Selection = random.choice(self.stages)
    
    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Battle Mode Map Selector', 
                          description = 'Randomly selects one of the eight maps in Battle Mode', 
                          color = discord.Color.random())

    embed.add_field(name = 'Map Selected!', value = Selection)
    embed.set_footer(text = 'If an unfavorable map, reroll')
    
    await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot):
  await bot.add_cog(MK8BattleMap(bot))