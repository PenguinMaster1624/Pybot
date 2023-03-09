from discord.ext import commands
from discord import app_commands
import random, discord

class pbgm_buttons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = 360)

  async def on_timeout(self):
    for item in self.children:
      item.disabled = True

  @discord.ui.button(label = 'Reroll', style = discord.ButtonStyle.blurple)
  async def reroll(self, interaction = discord.Interaction, button = discord.ui.Button):
    await pbgm.pbgm.callback(self, interaction)
  
  @discord.ui.button(label = 'Quit', style = discord.ButtonStyle.danger)
  async def quit(self, interaction = discord.Interaction, button = discord.ui.Button):
    for item in self.children:
      item.disabled = True

    await interaction.response.edit_message(content = 'Happy Gaming!', embed = None, view = self)

class pbgm(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.private_battle_modes = ['Turf War', 'Splat Zones', 'Rainmaker', 'Tower Control', 'Clam Blitz']
    
  @app_commands.command(name = 'pbgm', description = 'Rolls a random Splatoon 3 game mode available in Private Battles')  
  async def pbgm(self, interaction: discord.Interaction):

    embed = discord.Embed(title = 'Splatoon 3 Game Mode Randomizer', description = 'Randomly chooses a game mode to play', color = discord.Color.random())
    embed.add_field(name = 'Game Mode Selected!', value = f'{random.choice(self.private_battle_modes)}')
    embed.set_footer(text = 'if unfavorable game mode, reroll')

    await interaction.response.send_message(embed = embed, ephemeral = True, view = pbgm_buttons())

async def setup(bot):
  await bot.add_cog(pbgm(bot))