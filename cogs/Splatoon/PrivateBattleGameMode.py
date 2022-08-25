from discord.ext import commands
import discord
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

    embed = discord.Embed(title = 'Splatoon 2 Game Mode Randomizer', description = 'Randomly chooses a game mode to play', color = discord.Color.random())
    embed.add_field(name = 'Game Mode Selected!', value = select)
    #embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    embed.set_footer(text = 'if unfavorable game mode, reroll')

    await ctx.reply(embed = embed)

async def setup(bot):
  await bot.add_cog(pbgm(bot))