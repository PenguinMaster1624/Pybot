import discord
from discord.ext import commands
from discord import app_commands
import random

class ButtonMK8DBattleStages(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = 360)
  
  async def on_timeout(self):
    for item in self.children:
      item.disabled = True

  @discord.ui.button(label = 'Reroll', style = discord.ButtonStyle.blurple)
  async def reroll(self, interaction = discord.Interaction, button = discord.ui.Button):
    await MK8BattleMap.mk8bm.callback(self, interaction)
  
  @discord.ui.button(label = 'Quit', style = discord.ButtonStyle.danger)
  async def quit(self, interaction = discord.Interaction, button = discord.ui.Button):
    for item in self.children:
      item.disabled = True

    await interaction.response.edit_message(content = 'Happy Gaming!', embed = None)

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mk8bm', description = 'Rolls a random Mario Kart 8 Deluxe Battle Mode Map')
  async def mk8bm(self, interaction: discord.Interaction):

    stages = ['Dragon Palace', 'Battle Stadium', 'Lunar Colony', 'Wuhu Town', 'Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']
  
    random.shuffle(stages)
    Selection = random.choice(stages)
    
    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Battle Mode Map Selector', 
                          description = 'Randomly selects one of the eight maps in Battle Mode', 
                          color = discord.Color.random())

    embed.add_field(name = 'Map Selected!', value = Selection)
    embed.set_footer(text = 'If an unfavorable map, reroll')
    
    await interaction.response.send_message(embed = embed, view = ButtonMK8DBattleStages(), ephemeral = True)

async def setup(bot):
  await bot.add_cog(MK8BattleMap(bot))