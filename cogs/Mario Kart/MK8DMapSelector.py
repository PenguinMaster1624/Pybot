from discord.ext import commands
from discord import app_commands
import random, discord

class MK8Map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.mushroom = ['Mushroom Cup: Mario Kart Stadium', 'Mushroom Cup: Water Park', 'Mushroom Cup: Sweet Sweet Canyon', 'Mushroom Cup: Thwomp Ruins']
    self.flower = ['Flower Cup: Mario Circuit', 'Flower Cup: Toad Harbor', 'Flower Cup: Twisted Mansion', ' Flower Cup: Shy Guy Falls']
    self.star = ['Star Cup: Sunshine Airport', 'Star Cup: Dolphin Shoals', 'Star Cup: Electrodome', 'Star Cup: Mount Wario']
    self.special = ['Special Cup: Cloudtop Cruise', 'Special Cup: Bone-Dry Dunes', 'Special Cup: Bowser\'s Castle', 'Special Cup: Rainbow Road']
    self.shell = ['Shell Cup: Moo Moo Meadows', 'Shell Cup: Mario Circuit', 'Shell Cup: Cheep Cheep Beach', 'Shell Cup: Toad\'s Turnpike']
    self.banana = ['Banana Cup: Dry Dry Desert', 'Banana Cup: Donut Plains 3', 'Banana Cup: Royal Raceway', 'Banana Cup: DK Jungle']
    self.leaf = ['Leaf Cup: Wario Stadium', 'Leaf Cup: Sherbet Land', 'Leaf Cup: Music Park', 'Leaf Cup: Yoshi Valley']
    self.lightning = ['Lightning Cup: Tick-Tock Clock', 'Lightning Cup: Piranha Plant Slide', 'Lightning Cup: Grumble Volcano', 'Lightning Cup: Rainbow Road (N64)']
    self.egg = ['Egg Cup: Yoshi Circuit', 'Egg Cup: Excitebike Arena', 'Egg Cup: Dragon Driftway', 'Egg Cup: Mute City']
    self.crossing = ['Crossing Cup: Baby Park', 'Crossing Cup: Cheese Land', 'Crossing Cup: Wild Woods', 'Crossing Cup: Animal Crossing']
    self.triforce = ['Triforce Cup: Wario\'s Gold Mine', 'Triforce Cup: Rainbow Road (SNES)', 'Triforce Cup: Ice Ice Outpost', 'Triforce Cup: Hyrule Circuit']
    self.bell = ['Bell Cup: Neo Bowser City', 'Bell Cup: Ribbon Road', 'Bell Cup: Super Bell Subway', 'Bell Cup: Big Blue']
    self.golden_dash = ['Golden Dash Cup: Paris Promenade', 'Golden Dash Cup: Toad Circuit', 'Golden Dash Cup: Choco Mountain', 'Golden Dash Cup: Coconut Mall']
    self.lucky_cat = ['Lucky Cat Cup: Tokyo Blur', 'Lucky Cat Cup: Shroom Ridge', 'Lucky Cat Cup: Sky Garden', 'Lucky Cat Cup: Ninja Hideaway']
    self.turnip = ['Turnip Cup: New York Minute', 'Turnip Cup: Mario Circuit 3', 'Turnip Cup: Kalamari Desert', 'Turnip Cup: Waluigi Pinball']
    self.propeller = ['Propeller Cup: Sydney Sprint', 'Propeller Cup: Snow Land', 'Propeller Cup: Mushroom Gorge', 'Propeller Cup: Sky-High Sundae']
    self.rock = ['Rock Cup: London Loop', 'Rock Cup: Boo Lake', 'Rock Cup: Rock Rock Mountain', 'Rock Cup: Maple Treeway']
    self.moon = ['Moon Cup: Berlin Byways', 'Moon Cup: Peach Gardens', 'Moon Cup: Merry Mountain', 'Moon Cup: 3DS Rainbow Road']
    self.fruit = ['Fruit Cup: Amsterdam Drift', 'Fruit Cup: Riverside Park', 'Fruit Cup: DK Summit', 'Fruit Cup: Yoshi\'s Island']
    self.boomerang = ['Bomerang Cup: Bangkok Rush', 'Boomerang Cup: DS Mario Cirtuit', 'Boomerang Cup: Waluigi Stadium', 'Boomerang Cup: Singapore Speedway']
    self.general = list(self.mushroom + self.flower + self.star + self.special + self.shell + self.banana + self.leaf + self.lightning + self.egg + self.crossing + self.triforce + self.bell + self.golden_dash + self.lucky_cat + self.turnip + self.propeller + self.rock + self.moon + self.fruit + self.boomerang)

  @app_commands.command(name = 'mk8m', description = 'Rolls a random map from the available Mario Kart 8 Deluxe maps, includes DLC')
  async def mk8m(self, interaction: discord.Interaction, cup: str = 'General'):

    all_cups = {'Mushroom': self.mushroom, 'Flower': self.flower, 'Star': self.star, 'Special': self.special, 
                'Shell': self.shell, 'Banana': self.banana, 'Leaf': self.leaf, 'Lightning': self.lightning, 'Egg': self.egg, 'Crossing': self.crossing, 'Triforce': self.triforce, 'Bell': self.bell, 
                'Golden Dash': self.golden_dash, 'Lucky Cat': self.lucky_cat, 'Turnip': self.turnip, 'Propeller': self.propeller, 'Rock': self.rock, 'Moon': self.moon,'General': self.general,
                'Fruit': self.fruit, 'Boomerang': self.boomerang}
  
    if cup.title() in all_cups:
      if cup == 'General':
        random.shuffle(all_cups[cup])
        selection = random.choice(all_cups[cup])
        
      else:
        selection = random.choice(all_cups[cup])

      split = selection.split(': ')
      embed = discord.Embed(title = 'Mario Kart 8 Deluxe Map Selector', color = discord.Color.random())
      embed.add_field(name = split[1], value = split[0])

      await interaction.response.send_message(embed = embed, ephemeral = True)
        
    else:
      await interaction.response.send_message('Please specify one of the cups currently playable, the default\'s from a pool of every track to date. Maybe you misspelled something?')

  @mk8m.autocomplete('cup')
  async def mk8m_autocomplete(self, interaction: discord.Interaction, current: str)-> list[app_commands.Choice[str]]:
    cups = ['Mushroom', 'Flower', 'Star', 'Special', 'Shell', 'Banana', 'Leaf', 'Lightning', 'Egg', 'Crossing', 'Triforce', 'Bell', 'Golden Dash', 'Lucky Cat', 'Turnip', 'Propeller', 'Rock', 'Moon', 'Fruit', 'Boomerang']
    return [app_commands.Choice(name = cup, value = cup) for cup in cups if current.lower() in cup.lower()]

async def setup(bot):
  await bot.add_cog(MK8Map(bot))