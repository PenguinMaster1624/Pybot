from discord.ext import commands
from discord import app_commands
import requests, discord, re

class SkyblockItems(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mayor', description = 'Displays information on the current Hypixel Skyblock mayor')
  async def mayor(self, interaction: discord.Interaction):
    r = requests.get('https://api.hypixel.net/resources/skyblock/election') 
    
    if r.status_code == 200:
      mayor = r.json()['mayor']
      name = mayor['name']
      mayor_type = mayor['key']
      mayor_stuff = mayor['perks']
    
      # reformats the mayor type to have the first letter capitalized
      mayor_type = mayor_type.title()

      perk_names = set()
      perk_descriptions = set()

      # adds the current mayor's perk information to the corresponding sets
      for i in range(len(mayor_stuff)):
        perk_names.add(mayor_stuff[i]['name'])
        perk_descriptions.add(mayor_stuff[i]['description'])

      perk_names = list(perk_names)
      perk_descriptions = list(perk_descriptions)
      perk_buffs = []

      # removes simoleon and the following character for better readability
      for i in range(len(perk_descriptions)): 
        string = re.sub(r'§.', '', perk_descriptions[i])
        perk_buffs.append(string)

      # embed creation and setup
      embed = discord.Embed(title = 'Hypixel Skyblock\'s Current Mayor', color = discord.Color.random())
      embed.add_field(name = name, value = f'Specialization: {mayor_type}')

      # creates individual fields for the mayor's perks
      for i in range(len(perk_names)):
        embed.add_field(name = perk_names[i], value = perk_buffs[i], inline = False)

      embed.set_footer(text = 'The mayor is updated roughly every 5 days, 4 hours amd 48 minutes in real life')
      await interaction.response.send_message(embed = embed)
      
  @app_commands.command(name = 'election', description = 'Displays information on the current Hypixel Skyblock election')
  async def election(self, interaction: discord.Interaction):
    r = requests.get('https://api.hypixel.net/resources/skyblock/election')
    
    if r.status_code == 200:
      js = r.json()

      # checks if there is an ongoing election
      try:
        election = js['current']['candidates']  
      
      # if there isn't an ongoing election, it skips everything and states that there isn't one
      except KeyError:
        await interaction.response.send_message('There isn\'t an ongoing election')

      else:
        # individual lists that grab their respective values for each candidate from the API
        name = [i['name'] for i in election]
        slot = [i['perks'] for i in election]
        votes = [i['votes'] for i in election]
        mayor_type = [i['key'].title() for i in election]

        # creates lists for respective mayors and their perks, for use in the following for loop
        perk_name_one, perk_name_two, perk_name_three, perk_name_four, perk_name_five = [set() for i in range(5)]
        perk_description_one, perk_description_two, perk_description_three, perk_description_four, perk_description_five = [set() for i in range(5)]
  
        perk_names = [perk_name_one, perk_name_two, perk_name_three, perk_name_four, perk_name_five]
        perk_descriptions = [perk_description_one, perk_description_two, perk_description_three, perk_description_four, perk_description_five]
  
        # adds the candidates' perks to their respective mayors
        for i in range(len(slot)):
          for j in slot[i]:
            perk_names[i].add(j['name'])
            perk_descriptions[i].add(j['description'])

        for i in range(len(perk_names)):
          perk_names[i] = list(perk_names[i])
          perk_descriptions[i] = list(perk_descriptions[i])

        # removes the simoleon and the character following it, for better readability
        for i in range(len(perk_descriptions)):
          for j in range(len(perk_descriptions[i])):
            string = re.sub(r'§.', '', perk_descriptions[i][j])
            perk_descriptions[i][j] = string
        
        all_votes = f'{sum([int(votes[i]) for i in range(len(votes))]):,}'

        for i in range(len(votes)):
          votes[i] = f'{votes[i]:,}'

        # creation and setup of the embed
        embed = discord.Embed(title = 'Current Hypixel Skyblock Mayor Candidates', description = f'Total amount of votes: {all_votes}', color = discord.Color.random())
        
        # creates individual fields for each mayor and their perks
        for i in range(5):
          perk = '\n'.join(f'{name}\n{description}\n' for (name, description) in zip(perk_names[i], perk_descriptions[i]))
          embed.add_field(name = name[i], value = f'Specialization: {mayor_type[i]}\n\n{perk}\nVotes: {votes[i]}', inline = False)
            
        await interaction.response.send_message(embed = embed)

  @app_commands.command(name = 'bz', description = 'Displays information of a specified item in Hypixel Skyblock\'s Bazaar')
  async def bz(self, interaction: discord.Interaction, item_name: str):
    r = requests.get('https://api.hypixel.net/skyblock/bazaar')

    if r.status_code == 200:
      data = r.json()['products']
      
      lst = []
      item = ''

      for letter in item_name:
        lst.append(letter)

        # changes any lowercase letters to uppercase and adds an underscore in place of spaces
        # this is done so in order to match the passed item to an id
        for lower in range(len(lst)):
          lst[lower] = lst[lower].upper()
          lst[lower] = re.sub(' ', '_', lst[lower])
        item += lst[lower]

      # if statement checks to see if the passed item -- processed -- exists in the bazaar
      if item in data:
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

      # if the passed item doesn't exist in the bazaar, this is sent
      # this is done in case of a typo
      else:
        await interaction.response.send_message('The bazaar doesn\'t sell that. Maybe there was a typo?')
      
    elif r.status_code == 503:
      await interaction.response.send_message('Data hasn\'t loaded yet, try again in a bit')

async def setup(bot):
  await bot.add_cog(SkyblockItems(bot))
