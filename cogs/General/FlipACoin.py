from discord.ext import commands
from discord import app_commands
import random, discord


class CoinButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = 10)

  async def on_timeout(self):
    for item in self.children:
      item.disabled = True

  @discord.ui.button(label = 'Reroll', style = discord.ButtonStyle.blurple)
  async def reroll(self, interaction = discord.Interaction, button = discord.ui.Button):
    await FlipCoin.fac.callback(self, interaction)
    
class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'fac', description = 'Flips a coin for you')
  async def fac(self, interaction: discord.Interaction):
    
    lst = ['Heads', 'Tails']

    choice = random.choice(lst)
    await interaction.response.send_message(choice, ephemeral = True, view = CoinButtons())

async def setup(bot):
  await bot.add_cog(FlipCoin(bot))