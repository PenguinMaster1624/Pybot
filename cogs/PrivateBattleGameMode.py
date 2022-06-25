from discord.ext import commands
import random

class pbgm(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()  
  async def pbgm(self, ctx):
    
    PrivateBattleModes = ['Turf War (Splatfest)', 'Turf War', 'Splat Zones', 'Rainmaker', 'Tower Control', 'Clam Blitz']

    Selection = []

    random.shuffle(PrivateBattleModes)
    Selection.append(random.choice(PrivateBattleModes))

    select = ''.join(Selection)

    await ctx.channel.send('Private Battle Game Mode: ' + select)

def setup(bot):
  bot.add_cog(pbgm(bot))