from discord.ext import commands
import random

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mk8bm(self, ctx):
    """Random Map Generator for Mario Kart 8 Deluxe's Battle Mode. Sure, it's got a random option, but this was fun to make"""
    
    lst = ['Dragon Palace', 'Battle Stadium', 'Lunar Colony', 'Wuhu Town', 'Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']

    random.shuffle(lst)
    Selection = random.choice(lst)
    
    await ctx.send(Selection)

def setup(bot):
  bot.add_cog(MK8BattleMap(bot))