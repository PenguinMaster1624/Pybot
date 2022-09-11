from discord.ext import commands
from discord import app_commands
import discord
import random

class pbgm(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @app_commands.command(name = 'pbgm', description = 'Rolls a random Splatoon 2 game mode available in Private Battles')  
  async def pbgm(self, interaction: discord.Interaction):
    
    PrivateBattleModes = ['Turf War (Splatfest)', 'Turf War', 'Splat Zones', 'Rainmaker', 'Tower Control', 'Clam Blitz']

    Selection = []

    random.shuffle(PrivateBattleModes)
    Selection.append(random.choice(PrivateBattleModes))

    select = ''.join(Selection)

    embed = discord.Embed(title = 'Splatoon 2 Game Mode Randomizer', description = 'Randomly chooses a game mode to play', color = discord.Color.random())
    embed.add_field(name = 'Game Mode Selected!', value = select)
    embed.set_footer(text = 'if unfavorable game mode, reroll')

    await interaction.response.send_message(embed = embed)

async def setup(bot):
  await bot.add_cog(pbgm(bot))