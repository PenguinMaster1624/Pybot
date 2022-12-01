import discord
from discord.ext import commands
from discord import app_commands
import random

class MK8DButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = 240)

  async def on_timeout(self):
    for item in self.children:
      item.disabled = True

  @discord.ui.button(label = 'Reroll', style = discord.ButtonStyle.blurple)
  async def reroll(self, interaction = discord.Interaction, button = discord.ui.Button):
    await MK8Map.mk8m.callback(self, interaction)

    await interaction.response.edit_message(content = 'Happy Gaming!', embed = None, view = self)

class MK8Map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mk8m', description = 'Rolls a random map from the available Mario Kart 8 Deluxe maps, includes DLC')
  async def mk8m(self, interaction: discord.Interaction, cup: str = 'General'):

    mushroom = ['Mushroom Cup: Mario Kart Stadium', 'Mushroom Cup: Water Park', 'Mushroom Cup: Sweet Sweet Canyon', 'Mushroom Cup: Thwomp Ruins']
    flower = ['Flower Cup: Mario Circuit', 'Flower Cup: Toad Harbor', 'Flower Cup: Twisted Mansion', ' Flower Cup: Shy Guy Falls']
    star = ['Star Cup: Sunshine Airport', 'Star Cup: Dolphin Shoals', 'Star Cup: Electrodome', 'Star Cup: Mount Wario']
    special = ['Special Cup: Cloudtop Cruise', 'Special Cup: Bone-Dry Dunes', 'Special Cup: Bowser\'s Castle', 'Special Cup: Rainbow Road']
    shell = ['Shell Cup: Moo Moo Meadows', 'Shell Cup: Mario Circuit', 'Shell Cup: Cheep Cheep Beach', 'Shell Cup: Toad\'s Turnpike']
    banana = ['Banana Cup: Dry Dry Desert', 'Banana Cup: Donut Plains 3', 'Banana Cup: Royal Raceway', 'Banana Cup: DK Jungle']
    leaf = ['Leaf Cup: Wario Stadium', 'Leaf Cup: Sherbet Land', 'Leaf Cup: Music Park', 'Leaf Cup: Yoshi Valley']
    lightning = ['Lightning Cup: Tick-Tock Clock', 'Lightning Cup: Piranha Plant Slide', 'Lightning Cup: Grumble Volcano', 'Lightning Cup: Rainbow Road (N64)']
    egg = ['Egg Cup: Yoshi Circuit', 'Egg Cup: Excitebike Arena', 'Egg Cup: Dragon Driftway', 'Egg Cup: Mute City']
    crossing = ['Crossing Cup: Baby Park', 'Crossing Cup: Cheese Land', 'Crossing Cup: Wild Woods', 'Crossing Cup: Animal Crossing']
    triforce = ['Triforce Cup: Wario\'s Gold Mine', 'Triforce Cup: Rainbow Road (SNES)', 'Triforce Cup: Ice Ice Outpost', 'Triforce Cup: Hyrule Circuit']
    bell = ['Bell Cup: Neo Bowser City', 'Bell Cup: Ribbon Road', 'Bell Cup: Super Bell Subway', 'Bell Cup: Big Blue']
    golden_dash = ['Golden Dash Cup: Paris Promenade', 'Golden Dash Cup: Toad Circuit', 'Golden Dash Cup: Choco Mountain', 'Golden Dash Cup: Coconut Mall']
    lucky_cat = ['Lucky Cat Cup: Tokyo Blur', 'Lucky Cat Cup: Shroom Ridge', 'Lucky Cat Cup: Sky Garden', 'Lucky Cat Cup: Ninja Hideaway']
    turnip = ['Turnip Cup: New York Minute', 'Turnip Cup: Mario Circuit 3', 'Turnip Cup: Kalamari Desert', 'Turnip Cup: Waluigi Pinball']
    propeller = ['Propeller Cup: Sydney Sprint', 'Propeller Cup: Snow Land', 'Propeller Cup: Mushroom Gorge', 'Propeller Cup: Sky-High Sundae']
    general = list(mushroom + flower + star + special + shell + banana + leaf + lightning + egg + crossing + triforce + bell + golden_dash + lucky_cat + turnip + propeller)

    all_cups = {'Mushroom': mushroom, 'Flower': flower, 'Star': star, 'Special': special, 'Shell': shell, 'Banana': banana, 'Leaf': leaf, 'Lightning': lightning, 'Egg': egg, 'Crossing': crossing, 'Triforce': triforce, 'Bell': bell, 'Golden Dash': golden_dash, 'Lucky Cat': lucky_cat, 'Turnip': turnip, 'Propeller': propeller, 'General': general}
  
    if cup in all_cups:
      if cup == 'General':
        random.shuffle(all_cups[cup])
        selection = random.choice(all_cups[cup])
        
      else:
        selection = random.choice(all_cups[cup])

      split = selection.split(': ')
      embed = discord.Embed(title = 'Mario Kart 8 Deluxe Map Selector', color = discord.Color.random())
      embed.add_field(name = split[1], value = split[0])

      await interaction.response.send_message(embed = embed, view = MK8DButtons(), ephemeral = True)
        
    else:
      await interaction.response.send_message('Please specify one of the cups currently playable, the default\'s from a pool of every track to date. Maybe you misspelled something?')

  @mk8m.autocomplete('cup')
  async def mk8m_autocomplete(self, interaction: discord.Interaction, current: str)-> list[app_commands.Choice[str]]:
    cups = ['Mushroom', 'Flower', 'Star', 'Special', 'Shell', 'Banana', 'Leaf', 'Lightning', 'Egg', 'Crossing', 'Triforce', 'Bell', 'Golden Dash', 'Lucky Cat', 'Turnip', 'Propeller']
    return [app_commands.Choice(name = cup, value = cup) for cup in cups if current.lower() in cup.lower()]

async def setup(bot):
  await bot.add_cog(MK8Map(bot))