import random
from discord.ext import commands
from discord import app_commands
import discord


class CoinButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = 10)

  async def on_timeout(self):
    for item in self.children:
      item.disabled = True

  @discord.ui.button(label = 'Reroll', style = discord.ButtonStyle.blurple)
  async def reroll(self, interaction = discord.Interaction, button = discord.ui.Button):
    await FlipCoin.fac.callback(self, interaction)
  
  @discord.ui.button(label = 'Quit', style = discord.ButtonStyle.danger)
  async def quit(self, interaction = discord.Interaction, button = discord.ui.Button):
    for item in self.children:
      item.disabled = True

    await interaction.response.edit_message(content = 'Happy Gaming!', embed = None)

class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'fac', description = 'Flips a coin for you')
  async def fac(self, interaction: discord.Interaction):
    
    lst = ['Heads', 'Tails']

    Choice = random.choice(lst)
    await interaction.response.send_message(Choice, ephemeral = True, view = CoinButtons())

async def setup(bot):
  await bot.add_cog(FlipCoin(bot))