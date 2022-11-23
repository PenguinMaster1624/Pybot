from discord.ext import commands
from discord import app_commands
import requests
import discord
import re

class SkyblockItems(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mayor', description = 'Displays information on the current Hypixel Skyblock mayor')
  async def mayor(self, interaction: discord.Interaction):
    r = requests.get('https://api.hypixel.net/resources/skyblock/election') 
    
    if r.status_code == 200:
      mayor = r.json()['mayor']
      name = mayor['name']
      mayor_stuff = mayor['perks']
    
      temp_perk_name = []
      temp_perk_description = []
      perk_names = []
      perk_descriptions = []

      # appends the current mayor's perk information to the corresponding lists
      for i in range(len(mayor_stuff)):
        temp_perk_name.append(mayor_stuff[i]['name'])
        temp_perk_description.append(mayor_stuff[i]['description'])
        
        for j in range(len(temp_perk_name)):
          perk_names.append(temp_perk_name[j])
          perk_descriptions.append(temp_perk_description[j])
        
        temp_perk_name = []
        temp_perk_description = []

      perk_buffs = []
      
      # removes simoleon and the following character for better readability
      for i in range(len(perk_descriptions)): 
        string = re.sub(r'§.', '', perk_descriptions[i])
        perk_buffs.append(string)

      # embed creation and setup
      embed = discord.Embed(title = 'Hypixel Skyblock\'s Current Mayor', color = discord.Color.random())
      embed.add_field(name = name, value = 'The current mayor')

      # creates individual fields for the mayor's perks
      for i in range(len(perk_names)):
        embed.add_field(name = perk_names[i], value = perk_buffs[i], inline = False)

      embed.set_footer(text = 'The mayor is updated roughly every 5 days, 4 hours amd 48 minutes in real life')
      await interaction.response.send_message(embed = embed)
      
  @app_commands.command(name = 'election', description = 'Displays information on the current Hypixel Skyblock election')
  async def election(self, interaction: discord.Interaction):
    r = requests.get('https://api.hypixel.net/resources/skyblock/election')
    lst = []
    if r.status_code == 200:
      js = r.json()

      # checks if there is an ongoing election
      if 'current' in js:
        election = js['current']['candidates']  

        # gets candidate information and pretty much puts it all in one list
        for candidate in election:
          for i in candidate.values():
            lst.append(i)

        # individual lists that grab their respective values for each candidate
        Name = [lst[1], lst[5], lst[9], lst[13], lst[17]]
        Slot = [lst[2], lst[6], lst[10], lst[14], lst[18]]
        Votes = [lst[3], lst[7], lst[11], lst[15], lst[19]]

        # creates lists for respective mayors and their perks, for use in the following for loop
        perk_name_one = []
        perk_name_two = []
        perk_name_three = []
        perk_name_four = []
        perk_name_five = []
        
        perk_description_one = []
        perk_description_two = []
        perk_description_three = []
        perk_description_four = []
        perk_description_five = []
  
        perk_names = [perk_name_one, perk_name_two, perk_name_three, perk_name_four, perk_name_five]
        perk_descriptions = [perk_description_one, perk_description_two, perk_description_three, perk_description_four, perk_description_five]
  
        temp_names = []
        temp_descriptions = []

        # appends the candidates' perks to their respective mayors
        for i in range(len(Slot)):
          for j in Slot[i]:
            temp_names.append(j['name'])
            temp_descriptions.append(j['description'])
  
          for k in range(len(temp_names)):
            perk_names[i].append(temp_names[k])
            perk_descriptions[i].append(temp_descriptions[k])
  
          temp_names = []
          temp_descriptions = []

        del temp_names
        del temp_descriptions

        # removes the simoleon and the character following it, for better readability
        for i in range(len(perk_descriptions)):
          for j in range(len(perk_descriptions[i])):
            string = re.sub(r'§.', '', perk_descriptions[i][j])
            perk_descriptions[i][j] = string

        for i in range(len(Votes)):
          Votes[i] = '{:,}'.format(Votes[i])

        # creation and setup of the embed
        embed = discord.Embed(title = 'Current Hypixel Skyblock Mayor Candidates', 
                              color = discord.Color.random())
  
        #embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        # creates individual fields for each mayor and their perks
        for i in range(len(perk_names)):
          Perk = '\n'.join(f'{name}\n{description}\n' for (name, description) in zip(perk_names[i], perk_descriptions[i]))
          embed.add_field(name = Name[i], value = f'{Perk}\nVotes: {Votes[i]}', inline = False)
            
        await interaction.response.send_message(embed = embed)

      # if there isn't an ongoing election, it skips everything above and states that there isn't one
      else:
        await interaction.response.send_message('There isn\'t an ongoing election')

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
        
        buy_offer_price = item_info['sell_summary'][0]['pricePerUnit']
        sell_offer_price = item_info['buy_summary'][0]['pricePerUnit']

        # gets the amount being offered or ordered for the top offer/order
        # also how many orders are at the top
        buy_offer_amount = item_info['sell_summary'][0]['amount']
        sell_offer_amount = item_info['buy_summary'][0]['amount']

        buy_offer_order_num = item_info['sell_summary'][0]['orders']
        sell_offer_order_num = item_info['buy_summary'][0]['orders']

        # combined all of the prices and runs it through a for loop for formating
        prices = [instant_buy_price, instant_sell_price, buy_offer_price, sell_offer_price]

        for i in range(len(prices)):
          prices[i] = round(float(prices[i]), 1)
          prices[i] = '{:,}'.format(prices[i])

        buy_offer_amount = '{:,}'.format(buy_offer_amount)
        sell_offer_amount = '{:,}'.format(sell_offer_amount)

        buy_offer_order_num = '{:,}'.format(buy_offer_order_num)
        sell_offer_order_num = '{:,}'.format(sell_offer_order_num)

        bazaar_info = f'Instant Buy Price: {prices[0]}\nInstant Sell Price: {prices[1]}\n\nTop Buy Order Price: {prices[2]}\nTop Buyer Amount Requested: {buy_offer_amount}\nNumber Of Top Buyers: {buy_offer_order_num}\n\nTop Sell Offer Price: {prices[3]}\nTop Seller Amount Offered: {sell_offer_amount}\nNumber Of Top Sellers: {sell_offer_order_num}'
        
        #setup of embed
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