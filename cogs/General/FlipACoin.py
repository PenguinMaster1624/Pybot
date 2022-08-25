import random
from discord.ext import commands

class FlipCoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def fac(self, ctx):
    
    lst = ['Heads', 'Tails']

    Choice = random.choice(lst)
    await ctx.channel.send(Choice)

async def setup(bot):
  await bot.add_cog(FlipCoin(bot))