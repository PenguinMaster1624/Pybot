from discord.ext import commands
from discord import app_commands
import discord
import random

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

    self.Shooter = ['Splattershot Jr.', 'Splattershot', 'Splattershot Pro', 'Aerospray', 'N-ZAP', '.52 Gal', '.96 Gal' 'Jet Squelcher', 'L-3 Nozzlenose', ' H-3 Nozzlenose','Sploosh-O-Matic', 'Splash-O-Matic', 'Squeezer']
    self.Roller = ['Splat Roller', 'Carbon Roller', 'Flinza Roller', 'Dynamo Roller']
    self.Charger = ['Splat Charger', 'Squiffer', 'E-Liter', 'Bamboozler', 'Goo Tuber']
    self.Slosher = ['Slosher', 'Tri Slosher', 'Sloshing Machine', 'Explosher', 'Boblobber']
    self.Dualies = ['Splat Dualies', 'Dualie Squelchers', 'Tetra Dualies', 'Dapple Dualies', 'Glooga Dualies']
    self.Brella = ['Splat Brella', 'Tenta Brella', 'Undercover Brella']
    self.Blaster = ['Blaster', 'Range Blaster', 'Luna Blaster', 'Rapid Blaster', 'Clash Blaster']
    self.Brush = ['Inkbrush', 'OctoBrush']
    self.Splatling = ['Heavy Splatling', 'Mini Splatling', 'Hydra Splatling', 'Ballpoint Splatling', 'Nautilus']
    self.Splatana = ['Splatana Wiper', 'Splatana Stamper']
    self.Bow = ['Tri Stringer', 'REEFLUX 450']
    self.General = list(self.Shooter + self.Roller + self.Charger + self.Slosher + self.Dualies + self.Brella + self.Blaster + self.Brush + self.Splatling)

    self.Class = {'Shooter': self.Shooter, 'Roller': self.Roller, 'Charger': self.Charger, 'Slosher': self.Slosher, 'Dualies': self.Dualies, 'Bow': self.Bow, 
                  'Brella': self.Brella, 'Blaster': self.Blaster, 'Brush': self.Brush, 'Splatling': self.Splatling, 'General': self.General, 'Splatana': self.Splatana}


  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = 'General'):
    
    try:
      selection = random.choice(self.Class[weapon_class])

    except KeyError:
      await interaction.response.send_message('Something went wrong. Maybe you misspelled something?', ephemeral = True)
    
    else:
      embed = discord.Embed(title = 'Splatoon 3 Random Weapon Line Selector', description = 'Scopes go with their respective charger kits', color = discord.Color.random())
      embed.add_field(name = 'Weapon Line:', value = selection)
      embed.set_footer(text = 'You can choose any weapon kit with the name above')
      await interaction.response.send_message(embed = embed, ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Dualies', 'Brella', 'Blaster', 'Brush', 'Splatling', 'Splatana', 'Bow']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 2 weapon based on Sub Weapon')
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    SplatBomb = ['Inkbrush', 'Sploosh-o-matic 7', 'Tri Slosher Nouveau', 'Clash Blaster', 'Luna Blaster', 'Splattershot Jr.', 'Undercover Sorella Brella', 'Kensa Splat Roller', 'Octo Shot Replica', 'Tentatek Splattershot', 'Soda Slosher', 'Custom Dualie Squelchers', 'Kensa Splattershot Pro', 'Gold Dynamo Roller', 'Foil Squeezer', 'Splat Charger', 'Hero Charger Replica', 'Splatterscope']
    BurstBomb = ['Carbon Roller Deco', 'Tri Slosher', 'Aerospray PG', 'Neo Splash-o-matic', 'Splat Dualies', 'Hero Dualie Replicas', 'Splattershot', 'Hero Shot Replica', 'L-3 Nozzlenose D', 'Mini Splatling', 'Grim Range Blaster', 'Custom Jet Squelcher']
    SuctionBomb = ['Kensa Octobrush', 'Aerospray MG', 'Kensa Splat Dualies', 'N-ZAP \'85', 'Kensa Splattershot', 'Foil Flingza Roller', 'Slosher', 'Hero Slosher Replica', 'Rapid Blaster Deco', 'H-3 Nozzlenose D', 'Range Blaster', 'Forge Splattershot Pro', 'Nautilus 79', 'Fresh Squiffer', 'Goo Tuber']
    CurlingBomb = ['Emperry Splat Dualies', 'Zink Mini Splatling', 'Custom Goo Tuber', 'Bamboozler 14 Mk I', 'Splat Roller', 'Hero Roller Replica', 'Clash Blaster Neo', 'Sploosh-o-matic']
    AutoBomb = ['Carbon Roller', 'Octobrush', 'Herobrush Replica', 'Custom Splattershot Jr.', 'Sorella Brella', 'N-ZAP \'89', 'Custom Blaster', 'Dark Tetra Dualies', 'Sloshing Machine', 'New Squiffer', 'Hydra Splatling']
    InkMine = ['Inkbrush Nouveau', 'Luna Blaster Neo', 'Undercover Brella', 'Tenta Camo Brella', 'Glooga Dualies', 'Rapid Blaster', 'Dynamo Roller', 'Custom Hydra Splatling', 'E-Liter 4K', 'E-Liter 4K Scope']
    ToxicMist = ['Dapple Dualies Nouveau', 'Splash-o-matic', 'Blaster', 'Hero Blaster Replica', 'Kensa Mini Splatling', 'Rapid Blaster Pro', 'Bamboozler 14 Mk II', 'Jet Squelcher', 'Ballpoint Splatling']
    PointSensor = ['.52 Gal', 'Sloshing Machine Neo', 'Dualie Squelchers', 'H-3 Nozzlenose', 'Splattershot Pro', 'Nautilus 47', 'Classic Squiffer', 'Custom Explosher', 'Heavy Splatlin Remix']
    SplashWall = ['Kensa .52 Gal', 'Kensa L-3 Nozzlenose', 'Flinza Roller', 'Tenta Brella', 'Bloblobber', 'Glooga Dualies Deco', 'Kensa Cherry H-3 Nozzlenose', '.96 Gal', 'Rapid Blaster Pro Deco', 'Squeezer', 'Heavy Splatling Deco', 'Firefin Splat Charger', 'Firefin Splatterscope']
    Sprinkler = ['Permanent Inkbrush', 'Aerospray RG', 'Splat Brella', 'Hero Brella Replica', 'N-ZAP \'83', 'Light Tetra Dualies', 'Slosher Deco', 'Bloblobber Deco', '96 Gal', 'Kensa Dynamo Roller', 'Explosher', 'Heavy Splatling', 'Hero Splatling Replica', 'Kensa Charger', 'Kensa Splatterscope']
    SquidBeakon = ['Neo Sploosh-o-matic', 'Dapple Dualies', 'Octobrush Nouveau', 'Krak-On Splat Roller', 'Tenta Brella', 'Ballpoint Splatling Nouveau', 'Custom E-Liter 4K', 'Custom E-Liter 4K Scope']
    FizzyBomb = ['Kensa Luna Blaster', 'Kensa Sloshing Machine', 'Kensa Glooga Dualies', 'Bamboozler 14 Mk III']
    Torpedo = ['Clear Dapple Dualies', 'Kensa Splattershot Jr.', 'Kensa Undercover Brella', 'Kensa Rapid Blaster']

    SubWeapons = {'Splat Bomb': SplatBomb, 'Burst Bomb': BurstBomb, 'Suction Bomb': SuctionBomb, 'Curling Bomb': CurlingBomb, 'Auto Bomb': AutoBomb, 'Ink Mine': InkMine, 'Toxic Mist': ToxicMist, 
                  'Point Sensor': PointSensor, 'Splash Wall': SplashWall, 'Sprinkler': Sprinkler, 'Squid Beakon': SquidBeakon, 'Fizzy Bomb': FizzyBomb, 'Torpedo': Torpedo}

    try:
      sub_weapon = sub_weapon.strip()
      selection = random.choice(SubWeapons[sub_weapon])
    
    except KeyError:
      await interaction.response.send_message('Try again, I think you mispelled something. Don\'t forget to capitalize all words.', ephemeral = True)

    else:
      embed = discord.Embed(title = 'Splatoon 2 Weapon Randomizer Through Sub Weapon', color = discord.Color.random())
      embed.add_field(name = 'Weapon Selected!', value = selection)
      embed.set_footer(text = 'If disliked weapon, reroll')

      await interaction.response.send_message(embed = embed, ephemeral = True)

  @rss.autocomplete('sub_weapon')
  async def rss_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    subs = ['Splat Bomb', 'Burst Bomb', 'Suction Bomb', 'Curling Bomb', 'Auto Bomb', 'Ink Mine', 'Toxic Mist', 'Point Sensor', 'Splash Wall' , 'Sprinkler', 'Squid Beakon', 'Fizzy Bomb', 'Torpedo']
    return [app_commands.Choice(name = sub_weapon, value = sub_weapon) for sub_weapon in subs if current.lower() in sub_weapon.lower()]
      
  @app_commands.command(name = 'rsp', description = 'Rolls a random Splatoon 2 weapon based on Special')
  async def rsp(self, interaction: discord.Interaction, special: str):
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
      special = special.strip()
      selection = random.choice(Specials[special])

    except KeyError:
      await interaction.response.send_message('Try again, maybe there was a typo somewhere', ephemeral = True)

    else:
      embed = discord.Embed(title = 'Splatoon 2 Weapon Randomizer Through Special', description = f'{special} go brrr', color = discord.Color.random())
      embed.add_field(name = 'Weapon Selected!', value = selection)
      embed.set_footer(text = 'If disliked weapon, reroll')
      
      await interaction.response.send_message(embed = embed, ephemeral = True)
  
  @rsp.autocomplete('special')
  async def rsp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    specials = ['Tenta Missiles', 'Sting Ray', 'Inkjet', 'Splashdown', 'Ink Armor', 'Splat Bomb Launcher', 'Suction Bomb Launcher', 'Burst Bomb Launcher', 'Curling Bomb Launcher', 'Auto Bomb Launcher', 'Ink Storm', 'Baller', 'Bubble Blower', 'Booyah Bomb', 'Ultra Stamp']
    return [app_commands.Choice(name = special, value = special) for special in specials if current.lower() in special.lower()]
  

async def setup(bot: commands.Bot):
  await bot.add_cog(Splat2nRandomWeapon(bot), guild = None)