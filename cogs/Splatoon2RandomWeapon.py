from pydoc import describe
from tokenize import Special
from discord.ext import commands
import discord
import random

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def rsw(self, ctx, WeaponClass = 'General'):
    
    Shooter = ['Splattershot Jr.', 'Splattershot', 'Splattershot Pro', 'Aerospray', 'N-ZAP', '.52 Gal', '.96 Gal' 'Jet Squelcher', 'L-3 Nozzlenose', ' H-3 Nozzlenose','Sploosh-O-Matic', 'Splash-O-Matic', 'Squeezer']
    Roller = ['Splat Roller', 'Carbon Roller', 'Flinza Roller', 'Dynamo Roller']
    Charger = ['Splat Charger', 'Squiffer', 'E-Liter', 'Bamboozler', 'Goo Tuber']
    Slosher = ['Slosher', 'Tri Slosher', 'Sloshing Machine', 'Explosher', 'Boblobber']
    Dualies = ['Splat Dualies', 'Dualie Squelchers', 'Tetra Dualies', 'Dapple Dualies', 'Glooga Dualies']
    Brella = ['Splat Brella', 'Tenta Brella', 'Undercover Brella']
    Blaster = ['Blaster', 'Range Blaster', 'Luna Blaster', 'Rapid Blaster', 'Clash Blaster']
    Brush = ['Inkbrush', 'OctoBrush']
    Splatling = ['Heavy Splatling', 'Mini Splatling', 'Hydra Splatling', 'Ballpoint Splatling', 'Nautilus']
    Hero = ['Hero Shot', 'Hero Roller', 'Hero Charger', 'Hero Dualies', 'Hero Brella', 'Hero Splatling', 'Hero Blaster', 'Hero Brush']
    General = list(Shooter + Roller + Charger + Slosher + Dualies + Brella + Blaster + Brush + Splatling)

    Class = {'Shooter': Shooter, 'Roller': Roller, 'Charger': Charger, 'Slosher': Slosher, 'Dualies': Dualies,
             'Brella': Brella, 'Blaster': Blaster, 'Brush': Brush, 'Splatling': Splatling, 'Hero': Hero, 'General': General,
            'shooter': Shooter, 'roller': Roller, 'charger': Charger, 'slosher': Slosher, 'dualies': Dualies,
             'brella': Brella, 'blaster': Blaster, 'brush': Brush, 'splatling': Splatling, 'hero': Hero, 'general': General}

    try:
      Selection = []
      Selection.append(random.choice(Class[WeaponClass]))
      select = ''.join(Selection)

    except KeyError:
      await ctx.send('Something went wrong. Maybe you misspelled something?')
    
    else:
      embed = discord.Embed(title = 'Splatoon 2 Random Weapon Line Selector', description = 'Scopes go with their respective charger lines', color = discord.Color.random())
      embed.add_field(name = 'Weapon Line:', value = select)
      embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
      embed.set_footer(text = 'You can choose any weapon within the line')
      await ctx.send(embed = embed)

  @commands.command()
  async def rsp(self, ctx, special):
    TentaMissiles = ['Neo Sploosh-o-matic', 'Kensa Splattershot', 'N-ZAP \'89', 'Jet Squelcher', 'Grim Range Blaster', 'Clash Blaster Neo', 'H-3 Nozzlenose', 'Foil Flingza Roller', 'Octobrush Nouveau', 'Bamboozler 14 Mk I', 'Slosher', 'Hero Slosher Replica', 'Mini Splatling', 'Splat Dualies', 'Hero Splat Dualies', 'Dualie Squelchers']
    StingRay = ['.52 Gal Deco', 'Custom Jet Squelcher', 'Squeezer', 'Clash Blaster', 'Dynamo Roller', 'Splat Charger', 'Hero Charger Replica', 'Splatterscope', 'Heavy Splatling', 'Hero Splatling Replica']
    Inkjet = ['Splash-o-matic', 'Tentatek Splattershot', 'Octo Shot Replica', 'Custom Blaster', 'Rapid Blaster Deco', 'L-3 Nozzlenose D', 'Octobrush', 'Hero Brush Replica', 'Fresh Squiffer', 'Custom Goo Tuber', 'Ballpoint Splatling', 'Nautilus 79', 'Emperry Splat Dualies', 'Glooga Dualies']
    Splashdown = ['Sploosh-o-matic', 'Splattershot', 'Hero Shot Replica', '.96 Gal Deco', 'Blaster', 'Hero Blaster Replica', 'Splat Roller', 'Hero Roller Replica', 'Inkbrush', 'Goo Tuber', 'Kensa Sloshing Machine', 'Hydra Splatling', 'Clear Dapple Dualies', 'Dark Tetra Dualies', 'Undercover Brella']
    InkArmor = ['Splattershot Jr.', '.96 Gal', 'N-ZAP \'85', 'Rapid Blaster Pro Deco', 'Gold Dynamo Roller', 'Permanent Inkbrush', 'Classic Squiffer', 'Tri Slosher', 'Custom Hydra Splatling', 'Kensa Glooga Dualies', 'Kensa Undercover Brella']
    SplatBombLauncher = ['Rapid Blaster', 'Flingza Roller', 'Sloshing Machine Neo', 'Sorella Brella']
    SuctionBombLauncher = ['Neo Splash-o-matic', 'Luna Blaster Neo', 'Firefin Splat Charger', 'Firefin Splatterscope', 'Bloblobber Deco', 'Dapple Dualies']
    BurstBombLauncher = ['Soda Slosher', 'Bamboozler 14 Mk II']
    CurlingBombLauncher = ['Aerospray MG', 'Tenta Sorella Brella']
    AutoBombLauncher = ['Carbon Roller Deco', 'Light Tetra Dualies']
    InkStorm = ['Custom Splattershot Jr.', 'N-ZAP \'83', 'Splattershot Pro', 'Kensa Luna Blaster', 'Range Blaster', 'Rapid Blaster Pro', 'Carbon Roller', 'E-Liter 4K', 'E-Liter 4K Scope', 'Tri Slosher Nouveau', 'Bloblobber', 'Zink Mini Splatling', 'Ballpoint Splatling Nouveau', 'Dapple Dualies Nouveau', 'Custom Jet Squelchers', 'Splat Brella', 'Hero Brella Replica']
    Baller = ['Aerospray RG', '.52 Gal', 'Luna Blaster', 'Kensa Rapid Blaster', 'L-3 Nozzlenose', 'Krak-On Splat Roller', 'Inkbrush Nouveau', 'New Squiffer', 'Kensa Charger', 'Kensa Splatterscope', 'Slosher Deco', 'Custom Explosher', 'Nautilus 47', 'Kensa Splat Dualies', 'Glooga Dualies Deco', 'Uncercover Sorella Brella']
    BubbleBlower = ['Kensa Splattershot Jr.', 'Forge Splattershot Pro', 'Foil Squeezer', 'Custom Range Blaster', 'Cherry H-3 Nozzlenose', 'Kensa Splat Roller', 'Custom E-Liter 4K', 'Custom E-Liter 4K Scope', 'Bamboozler 14 Mk III', 'Explosher', 'Heavy Splatling Deco', 'Tenta Brella']
    BooyahBomb = ['Aerospray PG', 'Kensa .52 Gal', 'Kensa Splattershot Pro', 'Kensa Dynamo Roller', 'Heavy Splatling Remix']
    UltraStamp = ['Sploosh-o-matic 7', 'Kensa L-3 Nozzlenose', 'Kensa Octobrush', 'Kensa Mini Splatling', 'Tenta Camo Brella']

    Specials = {'Tenta Missiles': TentaMissiles, 'Sting Ray': StingRay, 'Inkjet': Inkjet, 'Splashdown': Splashdown, 'Ink Armor': InkArmor, 'Splat Bomb Launcher': SplatBombLauncher,
                'Suction Bomb Launcher': SuctionBombLauncher, 'Burst Bomb Launcher': BurstBombLauncher, 'Curling Bomb Launcher': CurlingBombLauncher, 'Auto Bomb Launcher': AutoBombLauncher,
                'Ink Storm': InkStorm, 'Baller': Baller, 'Bubble Blower': BubbleBlower, 'Booyah Bomb': BooyahBomb, 'Ultra Stamp': UltraStamp}


    try:
      selection = []
      special = special.strip()
      selection.append(random.choice(Specials[special]))
      select = ''.join(selection)

    except KeyError:
      await ctx.send('Try again, maybe there was a typo somewhere')

    else:
      embed = discord.Embed(title = 'Splatoon 2 Weapon Randomizer With Specific Special', description = f'{special} go brrr', color = discord.Color.random())
      embed.add_field(name = 'Weapon Selected!', value = select)
      embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
      embed.set_footer(text = 'If disliked weapon, reroll')
      await ctx.send(embed = embed)

  @rsp.error
  async def rsp_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send('You might\'ve forgetten to add something')
    
    elif isinstance(error, commands.ExpectedClosingQuoteError):
      await ctx.send('Close the message with a double quote buddy')
    

def setup(bot):
  bot.add_cog(Splat2nRandomWeapon(bot))