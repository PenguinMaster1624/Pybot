from discord.ext import commands
from discord import app_commands
import requests, discord, re
import aiohttp

class SkyblockItems(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mayor', description = 'Displays information on the current Hypixel Skyblock mayor')
  async def mayor(self, interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://api.hypixel.net/resources/skyblock/election') as response:
        r = await response.json()
    
    if response.status != 200:
      await interaction.response.send_message('Data is inacessible')
      return
    
    mayor = r['mayor']
    name = mayor['name']
    mayor_type: str = mayor['key']
    mayor_stuff = mayor['perks']
    
    # reformats the mayor type to have the first letter capitalized
    mayor_type = mayor_type.title()
    perks = {}

    # adds the current mayor's perk information to the corresponding sets
    for i in range(len(mayor_stuff)):
      filtered_desc = re.sub(r'§.', '', mayor_stuff[i]['description'])
      perks[mayor_stuff[i]['name']] = filtered_desc

    # embed creation and setup
    embed = discord.Embed(title = 'Hypixel Skyblock\'s Current Mayor', color = discord.Color.random())
    embed.add_field(name = name, value = f'Specialization: {mayor_type}')

    # creates individual fields for the mayor's perks
    for perk, description in perks.items():
      embed.add_field(name = perk, value = description, inline = False)
    
    embed.set_footer(text = 'The mayor is updated roughly every 5 days, 4 hours amd 48 minutes in real life')
    await interaction.response.send_message(embed = embed)
      
  @app_commands.command(name = 'election', description = 'Displays information on the current Hypixel Skyblock election')
  async def election(self, interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://api.hypixel.net/resources/skyblock/election') as response:
        r = await response.json()
    
    if response.status == 200:

      # checks if there is an ongoing election
      try:
        election = r['current']['candidates']
      
      # if there isn't an ongoing election, it skips everything and states that there isn't one
      except KeyError:
        await interaction.response.send_message('There isn\'t an ongoing election')

      else:
        # individual lists that grab their respective values for each candidate from the API
        name = [mayor['name'] for mayor in election]
        slot = [mayor['perks'] for mayor in election]
        votes = [mayor['votes'] for mayor in election]
        mayor_type = [mayor['key'].title() for mayor in election]
        last_updated = r['lastUpdated']

        # creates lists for respective mayors and their perks, for use in the following for loop
        perks = [{} for i in range(5)]
  
        # adds the candidates' perks to their respective mayors
        for mayor in range(len(slot)):
          for perk in slot[mayor]:
            filtered_desc = re.sub(r'§.', '', perk['description'])
            perks[mayor][perk['name']] = filtered_desc
            
        percentages = []
        for i in range(len(votes)):
          percentages.append(round((int(votes[i])/sum(map(int, votes)))*100, 2))
        
        all_votes = f'{sum([int(votes[i]) for i in range(len(votes))]):,}'

        for i in range(len(votes)):
          votes[i] = f'{votes[i]:,}'

        # creation and setup of the embed
        embed = discord.Embed(title = 'Current Hypixel Skyblock Mayor Candidates', description = f'Last Updated: <t:{last_updated//1000}>, <t:{last_updated//1000}:R>', color = discord.Color.random())
        
        # creates individual fields for each mayor and their perks
        for i in range(5):
          perk = '\n'.join(f'__{name}__\n*{description}*\n' for name, description in perks[i].items())
          embed.add_field(name = name[i], value = f'Specialization: {mayor_type[i]}\n\n{perk}\nVotes: {votes[i]} (**{percentages[i]}%**)', inline = False)
        
        embed.set_footer(text = f'Total amount of votes: {all_votes}')
        await interaction.response.send_message(embed = embed)

  @app_commands.command(name = 'bz', description = 'Displays information of a specified item in Hypixel Skyblock\'s Bazaar')
  async def bz(self, interaction: discord.Interaction, item_name: str):
    r = requests.get('https://api.hypixel.net/skyblock/bazaar')

    if r.status_code == 200:
      data = r.json()['products']
      item = item_name.upper().strip().replace(' ', '_')

      # if statement checks to see if the passed item -- processed -- exists in the bazaar
      if item not in data:
        await interaction.response.send_message('The bazaar doesn\'t sell that. Maybe there was a typo?')
        return 
      
      # gets all the prices
      item_info = data[item]
      item_quick = item_info['quick_status']
      instant_buy_price = item_quick['buyPrice']
      instant_sell_price = item_quick['sellPrice']
      
      buy_offer_price = item_info['buy_summary'][0]['pricePerUnit']
      sell_offer_price = item_info['sell_summary'][0]['pricePerUnit']

      # gets the amount being offered or ordered for the top offer/order
      # also how many orders are at the top
      buy_offer_amount = item_info['buy_summary'][0]['amount']
      sell_offer_amount = item_info['sell_summary'][0]['amount']

      # combined all of the prices and runs it through a for loop for formating
      prices = [instant_buy_price, instant_sell_price, buy_offer_price, sell_offer_price]

      for i in range(len(prices)):
        prices[i] = round(float(prices[i]), 1)
        prices[i] = '{:,}'.format(prices[i])

      buy_offer_amount = '{:,}'.format(buy_offer_amount)
      sell_offer_amount = '{:,}'.format(sell_offer_amount)

      bazaar_info = f'Instant Buy Price: {prices[0]}\nInstant Sell Price: {prices[1]}\n\nTop Buy Order Price: {prices[2]}\nTop Amount Wanted: {buy_offer_amount}\n\nTop Sell Offer Price: {prices[3]}\nTop Amount Offered: {sell_offer_amount}'
      
      # setup of embed
      embed = discord.Embed(title = 'Hypixel Skyblock Bazaar', color = discord.Color.random())
      embed.add_field(name = item, value = bazaar_info)
      
      await interaction.response.send_message(embed = embed)
      
    elif r.status_code == 503:
      await interaction.response.send_message('Data hasn\'t loaded yet, try again in a bit')
    
    else:
      await interaction.response.send_message('The data is inaccessible, the Hypixel API might be down')

async def setup(bot: commands.Bot):
  await bot.add_cog(SkyblockItems(bot))
