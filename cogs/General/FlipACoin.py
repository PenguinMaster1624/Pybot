import random
from discord.ext import commands
from discord import app_commands
import discord

class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'fac', description = 'Flips a coin for you')
  async def fac(self, interaction: discord.Interaction):
    
    lst = ['Heads', 'Tails']

    Choice = random.choice(lst)
    await interaction.response.send_message(Choice)

async def setup(bot):
  await bot.add_cog(FlipCoin(bot))