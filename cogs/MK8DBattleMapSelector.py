from discord.ext import commands
import random

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mk8bm(self, ctx):
    """Random Map Generator for MK8DX, cuz apparently it doesn't have one
       Mushroom, Flower, Star, Special, Shell, Banana, Leaf, Lightning,
       Egg, Crossing, Triforce, Bell, Golden Dash, Lucky Cat, General"""
    
    lst = ['Dragon Palace', 'Mario Stadium', 'Lunar Colony', 'Wuhu Town', 'SNES Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']

    random.shuffle(lst)
    Selection = random.choice(lst)
    
    await ctx.send(Selection)

def setup(bot):
  bot.add_cog(MK8BattleMap(bot))