from discord.ext import commands
from discord import app_commands
import random, discord


class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'fac', description = 'Flips a coin for you')
  async def fac(self, interaction: discord.Interaction):
    
    lst = ['Heads', 'Tails']

    choice = random.choice(lst)
    await interaction.response.send_message(choice, ephemeral = True)

async def setup(bot):
  await bot.add_cog(FlipCoin(bot))