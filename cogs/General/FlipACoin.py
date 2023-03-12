from discord.ext import commands
from discord import app_commands
import random, discord

class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sides = ['Heads', 'Tails']

  @app_commands.command(name = 'fac', description = 'Flips a coin for you')
  async def fac(self, interaction: discord.Interaction):

    choice = random.choice(self.sides)
    await interaction.response.send_message(choice, ephemeral = True)

async def setup(bot: commands.Bot):
  await bot.add_cog(FlipCoin(bot))