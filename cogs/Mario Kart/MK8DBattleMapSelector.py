import discord
from discord.ext import commands
import random

class MK8BattleMap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mk8bm(self, ctx):
    
    lst = ['Dragon Palace', 'Battle Stadium', 'Lunar Colony', 'Wuhu Town', 'Battle Course 1', 'Luigi\'s Mansion', 'Urchin Underpass', 'Sweet Sweet Kingdom']

    random.shuffle(lst)
    Selection = random.choice(lst)

    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Battle Mode Map Selector', 
                          description = 'Randomly selects one of the eight maps in Battle Mode', 
                          color = discord.Color.random())
    #embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    embed.add_field(name = 'Map Selected!', value = Selection)
    embed.set_footer(text = 'If an unfavorable map, reroll')
    
    await ctx.reply(embed = embed)

async def setup(bot):
  await bot.add_cog(MK8BattleMap(bot))