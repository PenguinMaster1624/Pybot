from discord.ext import commands
import requests
import discord
import re

class SkyblockItems(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mayor(self, ctx):
    r = requests.get('https://api.hypixel.net/resources/skyblock/election') 
    lst = []
    
    if r.status_code == 200:
      js = r.json()
      mayor = js['mayor']
      MayorName = mayor['name']
      MayorStuff = mayor['perks']
    
      TempPerkName = []
      TempPerkDesc = []
      PerkNames = []
      PerkDescriptions = []

      # appends the current mayor's perk information to the corresponding lists
      for i in range(len(MayorStuff)):
        TempPerkName.append(MayorStuff[i]['name'])
        TempPerkDesc.append(MayorStuff[i]['description'])
        
        for j in range(len(TempPerkName)):
          PerkNames.append(TempPerkName[j])
          PerkDescriptions.append(TempPerkDesc[j])
        
        TempPerkName = []
        TempPerkDesc = []

      string = ''

      PerkBuffs = []
      
      # removes simoleon and the following character for better readability
      for i in range(len(PerkDescriptions)): 
        string = re.sub(r'§.', '', PerkDescriptions[i])
        PerkBuffs.append(string)

      # embed creation and setup
      embed = discord.Embed(title = 'Hypixel Skyblock\'s Current Mayor', color = discord.Color.random())
      embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
      embed.add_field(name = MayorName, value = 'The current mayor')

      # creates individual fields for the mayor's perks
      for i in range(len(PerkNames)):
        embed.add_field(name = PerkNames[i], value = PerkBuffs[i], inline = False)

      embed.set_footer(text = 'The mayor is updated roughly every five days and four hours in real life')
        
      await ctx.send(embed = embed)
      
  @commands.command()
  async def election(self, ctx):
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
        MayorName = [lst[1], lst[5], lst[9], lst[13], lst[17]]
        MayorPerkSpot = [lst[2], lst[6], lst[10], lst[14], lst[18]]
        MayorVotes = [lst[3], lst[7], lst[11], lst[15], lst[19]]

        # creates lists for respective mayors and their perks, for use in the following for loop
        PerkNameOne = []
        PerkNameTwo = []
        PerkNameThree = []
        PerkNameFour = []
        PerkNameFive = []
        
        PerkDescriptionOne = []
        PerkDescriptionTwo = []
        PerkDescriptionThree = []
        PerkDescriptionFour = []
        PerkDescriptionFive = []
  
        PerkNames = [PerkNameOne, PerkNameTwo, PerkNameThree, PerkNameFour, PerkNameFive]
        PerkDescriptions = [PerkDescriptionOne, PerkDescriptionTwo, PerkDescriptionThree, PerkDescriptionFour, PerkDescriptionFive]
  
        TempNames = []
        TempDescs = []

        # appends the candidates' perks to their respective mayors
        for i in range(len(MayorPerkSpot)):
          for j in MayorPerkSpot[i]:
            TempNames.append(j['name'])
            TempDescs.append(j['description'])
  
          for k in range(len(TempNames)):
            PerkNames[i].append(TempNames[k])
            PerkDescriptions[i].append(TempDescs[k])
  
          TempNames = []
          TempDescs = []

        # removes the simoleon and the character following it, for better readability
        for i in range(len(PerkDescriptions)):
          for j in range(len(PerkDescriptions[i])):
            string = re.sub(r'§.', '', PerkDescriptions[i][j])
            PerkDescriptions[i][j] = string


        # creation and setup of the embed
        embed = discord.Embed(title = 'Current Hypixel Skyblock Mayor Candidates', 
                              color = discord.Color.random())
  
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        # creates individual fields for each mayor and their perks
        for i in range(len(PerkNames)):
          Perk = '\n'.join(f'{name}\n{description}\n' for (name, description) in zip(PerkNames[i], PerkDescriptions[i]))
          embed.add_field(name = MayorName[i], value = f'{Perk}\nVotes: {MayorVotes[i]}', inline = False)
            
        await ctx.send(embed = embed)

      # if there isn't an ongoing election, it skips everything above and states that there isn't one
      else:
        ctx.send('There isn\'t an ongoing election')
        
  @commands.command()
  async def ah(self, ctx):
    r = requests.get('https://api.hypixel.net/skyblock/auctions')

    if r.status_code == 200:
      pass
    
    elif r.status_code == 404:
      ctx.send('Page Not Found')

    elif r.status_code == 422:
      ctx.send('Invalid Page')

    elif r.status_code == 503:
      ctx.send('The data is not populated yet, try again shortly')

  @commands.command()
  async def bz(self, ctx, item):
    r = requests.get('https://api.hypixel.net/skyblock/bazaar')

    if r.status_code == 200:
      js = r.json()
  
    elif r.status_code == 503:
      ctx.send('Data hasn\'t loaded, try again in a bit')

def setup(bot):
  bot.add_cog(SkyblockItems(bot))