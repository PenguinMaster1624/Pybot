from models import MayoralResponse, BazaarResponse
from utils.sessions import fetch_data
from discord.ext import commands
from discord import app_commands
import discord 


class SkyblockItems(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mayor', description = 'Displays information on the current Hypixel Skyblock mayor')
  async def mayor(self, interaction: discord.Interaction):
    response = await fetch_data(url='https://api.hypixel.net/resources/skyblock/election', model=MayoralResponse)
    mayor_info = response.current_mayor

    mayor = discord.Embed(title=f'Current Mayor - {mayor_info.name}', color=discord.Color.random())
    for perk in mayor_info.perks:
      mayor.add_field(name=perk.name, value=perk.description, inline=False)

    mayor.set_footer(text=mayor_info.spec)

    minister = discord.Embed(title=f'Current Minister - {mayor_info.minister.name}', color=discord.Color.random())
    minister.add_field(name=mayor_info.minister.perks.name, value=mayor_info.minister.perks.description)
    minister.set_footer(text=mayor_info.minister.spec)
    
    await interaction.response.send_message(embeds=[mayor, minister], ephemeral=True)

  @app_commands.command(name = 'election', description = 'Displays information on the current Hypixel Skyblock election')
  async def election(self, interaction: discord.Interaction):
    response = await fetch_data(url='https://api.hypixel.net/resources/skyblock/election', model=MayoralResponse)
    election_info = response.current_election
    
    if election_info is None:
      await interaction.response.send_message('No election in session', ephemeral=True)
      return
    
    election = discord.Embed(title=f'Election For Year {election_info.year}')
    for candidate in election_info.candidates:
      election.add_field(name=f'{candidate.name} - {candidate.votes:,}', value=f'{candidate.spec}\n\n{candidate.perks}', inline=False)

    # finish embed setup and send the response message
    # suggest sending multiple embeds. Colors for each mayor TBD

  @app_commands.command(name = 'bz', description = 'Displays information of a specified item in Hypixel Skyblock\'s Bazaar')
  async def bz(self, interaction: discord.Interaction, item_name: str):
    ...

async def setup(bot: commands.Bot):
  await bot.add_cog(SkyblockItems(bot))
