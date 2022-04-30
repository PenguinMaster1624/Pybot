from discord.ext import commands
import random

class MK8Map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mk8m(self, ctx, Cup):
    """Random Map Generator for MK8DX, cuz apparently it doesn't have one
       Mushroom, Flower, Star, Special, Shell, Banana, Leaf, Lightning,
       Egg, Crossing, Triforce, Bell, Golden Dash, Lucky Cat, General"""
    
    Mushroom = ['Mushroom Cup: Mario Kart Stadium', 'Mushroom Cup: Water Park', 'Mushroom Cup: Sweet Sweet Canyon', 'Mushroom Cup: Thwomp Ruins']
    Flower = ['Flower Cup: Mario Circuit', 'Flower Cup: Toad Harbor', 'Flower Cup: Twisted Mansion', ' Flower Cup: Shy Guy Falls']
    Star = ['Star Cup: Sunshine Airport', 'Star Cup: Dolphin Shoals', 'Star Cup: Electrodome', 'Star Cup: Mount Wario']
    Special = ['Special Cup: Cloudtop Cruise', 'Special Cup: Bone-Dry Dunes', 'Special Cup: Bowser\'s Castle', 'Special Cup: Rainbow Road']
    Shell = ['Shell Cup: Moo Moo Meadows', 'Shell Cup: Mario Circuit', 'Shell Cup: Cheep Cheep Beach', 'Shell Cup: Toad\'s Turnpike']
    Banana = ['Banana Cup: Dry Dry Desert', 'Banana Cup: Donut Plains 3', 'Banana Cup: Royal Raceway', 'Banana Cup: DK Jungle']
    Leaf = ['Leaf Cup: Wario Stadium', 'Leaf Cup: Sherbet Land', 'Leaf Cup: Music Park', 'Leaf Cup: Yoshi Valley']
    Lightning = ['Lightning Cup: Tick-Tock Clock', 'Lightning Cup: Piranha Plant Slide', 'Lightning Cup: Grumble Volcano', 'Lightning Cup: Rainbow Road (N64)']
    Egg = ['Egg Cup: Yoshi Circuit', 'Egg Cup: Excitebike Arena', 'Egg Cup: Dragon Driftway', 'Egg Cup: Mute City']
    Crossing = ['Crossing Cup: Baby Park', 'Crossing Cup: Cheese Land', 'Crossing Cup: Wild Woods', 'Crossing Cup: Animal Crossing']
    Triforce = ['Triforce Cup: Wario\'s Gold Mine', 'Triforce Cup: Rainbow Road (SNES)', 'Triforce Cup: Ice Ice Outpost', 'Triforce Cup: Hyrule Circuit']
    Bell = ['Bell Cup: Neo Bowser City', 'Bell Cup: Ribbon Road', 'Bell Cup: Super Bell Subway', 'Bell Cup: Big Blue']
    GoldenDash = ['Golden Dash Cup: Paris Promenade', 'Golden Dash Cup: Toad Circuit', 'Golden Dash Cup: Choco Mountain', 'Golden Dash Cup: Coconut Mall']
    LuckyCat = ['Lucky Cat Cup: Tokyo Blur', 'Lucky Cat Cup: Shroom Ridge', 'Lucky Cat Cup: Sky Garden', 'Lucky Cat Cup: Ninja Hideaway']

    General = list(Mushroom + Flower + Star + Special + Shell + Banana + Leaf + Lightning + Egg + Crossing + Triforce + Bell + GoldenDash + LuckyCat)

    Dictionary = {'Mushroom' : Mushroom, 'Flower' : Flower, 'Star' : Star, 'Special' : Special, 'Shell' : Shell, 'Banana' : Banana, 'Leaf' : Leaf, 'Lightning' : Lightning,
                  'Egg' : Egg, 'Crossing' : Crossing, 'Triforce' : Triforce, 'Bell' : Bell, 'Golden Dash' : GoldenDash, 'Lucky Cat' : LuckyCat, 'General' : General}

    if Cup in Dictionary:
      if Cup == 'General':
        random.shuffle(Dictionary[Cup])
        Selection = random.choice(Dictionary[Cup])
      else:
        Selection = random.choice(Dictionary[Cup])
    else:
      await ctx.send('Please select one of the cups currently playable')
    
    await ctx.send(Selection)

def setup(bot):
  bot.add_cog(MK8Map(bot))