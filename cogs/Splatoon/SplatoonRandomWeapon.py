from discord.ext import commands
from discord import app_commands
import random, discord

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

    self.shooter = ['Splattershot Jr.', 'Splattershot', 'Splattershot Nova', 'Splattershot Pro', 'Aerospray', 'N-ZAP', '.52 Gal', '.96 Gal', 'Jet Squelcher', 'L-3 Nozzlenose', ' H-3 Nozzlenose','Sploosh-O-Matic', 'Splash-O-Matic', 'Squeezer']
    self.roller = ['Splat Roller', 'Carbon Roller', 'Big Swig Roller', 'Flinza Roller', 'Dynamo Roller']
    self.charger = ['Splat Charger', 'Splatterscope', 'Squiffer', 'E-Liter', 'Bamboozler', 'Goo Tuber', 'Snipewriter 5H']
    self.slosher = ['Slosher', 'Tri Slosher', 'Sloshing Machine', 'Explosher', 'Boblobber', 'Dread Wringer']
    self.splatling = ['Heavy Splatling', 'Mini Splatling', 'Hydra Splatling', 'Ballpoint Splatling', 'Nautilus', 'Heavy Edit Splatling']
    self.dualies = ['Splat Dualies', 'Dualie Squelchers', 'Tetra Dualies', 'Dapple Dualies', 'Glooga Dualies']
    self.brella = ['Splat Brella', 'Tenta Brella', 'Undercover Brella']
    self.blaster = ['Blaster', 'Range Blaster', 'Luna Blaster', 'Rapid Blaster', 'Rapid Blaster Pro', 'Clash Blaster', 'S-Blast \'92']
    self.brush = ['Inkbrush', 'Octobrush', 'Painbrush']
    self.bow = ['Tri-Stringer', 'REEF-LUX 450']
    self.splatana = ['Splatana Wiper', 'Splatana Stamper']
    self.general = list(self.shooter + self.roller + self.charger + self.slosher + self.splatling + self.dualies + self.brella + self.blaster + self.brush + self.bow + self.splatana)

    self.splat_bomb = ['Splattershot Jr.', 'Tentatek Splattershot', 'Luna Blaster', 'Clash Blaster', 'Inkbrush', 'Splat Charger', 'Splatterscope', 'Slosher', 'Dualie Squelchers', 'Gold Dynamo Roller']
    self.suction_bomb = ['Splattershot', 'Hero Shot Replica' , 'N-ZAP \'85', 'Forge Splattershot Pro', 'Range Blaster', 'Octobrush', 'Splat Dualies', 'Neo Splash-o-matic', 'Dread Wringer']
    self.burst_bomb = ['Splash-o-matic', 'Carbon Roller Deco', 'Mini Splatling', 'Splatana Stamper', 'L-3 Nozzlenose D']
    self.sprinkler = ['Aerospray RG', '.96 Gal', 'Dynamo Roller', 'Snipewriter 5H', 'Bloblobber', 'Heavy Splatling', 'Splat Brella', 'S-Blast \'92', 'Light Tetra Dualies', 'Inkline Tri-Stringer']
    self.splash_wall = ['.52 Gal', 'Squeezer', 'Big Swig Roller', 'Glooga Dualies', '.96 Gal Deco', 'Z+F Splat Charger', 'Z+F Splatterscope', 'H-3 Nozzlenose D', 'REEF-LUX 460 Deco', 'Snipewriter 5B']
    self.fizzy_bomb = ['Aerospray MG', 'Luna Blaster Neo', 'Sloshing Machine', 'Ballpoint Splatling', 'Tri Slosher Nouveau', 'Custom Goo Tuber']
    self.curling_bomb = ['Sploosh-o-matic', 'L-3 Nozzlenose', 'Splat Roller', 'REEF-LUX 450', 'Clash Blaster Neo', 'Heavy Edit Splatling', 'Painbrush', 'Emperry Splat Dualies']
    self.auto_bomb = ['Blaster', 'Carbon Roller', 'Bamboozler 14 Mk I', 'Hydra Splatling', 'Dark Tetra Dualies', 'N-ZAP \'89', 'Sorella Brella', 'Foil Squeezer']
    self.squid_beakon = ['Dapple Dualies', 'Tenta Brella', 'Neo Sploosh-o-matic', 'Krak-On Splat Roller', 'Splatana Wiper Deco', 'Octobrush Nouveau']
    self.point_sensor = ['Splattershot Nova', 'H-3 Nozzlenose', 'Classic Squiffer', 'Explosher', 'Nautilus 47', 'Painbrush Nouveau', 'Custom Blaster']
    self.ink_mine = ['Rapid Blaster', 'Flingza Roller', 'Inkbrush Nouveau', 'E-Liter 4K', 'E-Liter 4K Scope', 'Undercover Brella', 'Annaki Splattershot Nova', 'Tenta Sorella Brella', 'Ballpoint Splatling Nouveau']
    self.toxic_mist = ['Rapid Blaster Pro', 'Tri-Slosher', 'Zink Mini Splatling', 'Tri-Stringer', 'Custom Jet Squelcher', 'Neo Splatana Stamper']
    self.angle_shooter = ['Splattershot Pro', 'Jet Squelcher', 'Slosher Deco', 'Big Swig Roller Express', 'Rapid Blaster Pro Deco', 'Bloblobber Deco']
    self.torpedo = ['Custom Splattershot Jr.', 'Goo Tuber', 'Dapple Dualies Nouveau', 'Splatana Wiper', 'Rapidd Blaster Deco', 'Undercover Sorella Brella']

    self.trizooka = ['Splattershot', 'Hero Shot Replica', 'Clash Blaster', 'Squeezer', 'Carbon Roller Deco', 'Tenta Sorella Brella']
    self.big_bubbler = ['Splattershot Jr.', 'Blaster', 'Splat Roller', 'Classic Squiffer', 'Zink Mini Splatling', 'H-3 Nozzlenose D']
    self.zipcaster = ['Luna Blaster', 'Carbon Roller', 'Octobrush', 'Slosher Deco', 'Splatana Stamper', 'Light Tetra Dualies']
    self.tenta_missiles = ['Flingza Roller', 'Goo Tuber', 'REEF-LUX 450', 'Splatana Wiper Deco', 'Painbrush Nouveau']
    self.ink_storm = ['Bloblobber', 'Explosher', 'Nautilus 47', 'Custom Jet Squelcher', 'Big Swig Roller Express', 'Octobrush Nouveau', 'Snipewriter 5B']
    self.booyah_bomb = ['Aerospray RG', 'Forge Splattershot Pro', 'Sloshing Machine', 'Hydra Splatling', 'Glooga']
    self.wave_breaker = ['Custom Splattershot Jr.', 'Range Blaster', 'E-Liter 4K', 'E-Liter 4K Scope', 'Heavy Splatling', 'Dualie Squelchers', 'Painbrush']
    self.ink_vac = ['.96 Gal', 'Jet Squelcher', 'Rapid Blaster Pro', 'Big Swig Roller', 'Splat Charger', 'Splatterscope', 'Tenta Brella', 'Ballpoint Splatling Nouveau']
    self.killer_wail = ['.52 Gal', 'Splattershot Nova', 'Inkbrush', 'Bamboozler 14 Mk I', ' Tri-Stringer', 'Neo Sploosh-o-matic', 'Rapid Blaster Pro Deco']
    self.inkjet = ['Tri-Slosher', 'Ballpoint Splatling', 'Rapid Blaster Deco', 'Annaki Splattershot Nova', 'Sorella Brella']
    self.ultra_stamp = ['Sploosh-o-matic', 'Luna Blaster Neo', 'Inkbrush Nouveau', 'Mini Splatling', 'Mini Splatling', 'Splatana Wiper', 'L-3 Nozzlenose D', 'Custom Goo Tuber']
    self.crab_tank = ['Splash-o-matic', 'Splattershot Pro', 'L-3 Nozzlenose', 'Splat Dualies', 'Neo Splatana Stamper']
    self.reefslider = ['Aerospray MG', 'Dapple Dualies Nouveau', 'Dark Tetra Dualies', 'Undercover Brella', 'S-Blast \'92', 'Dread Wringer', 'REEF-LUX 450 Deco']
    self.tristrike = ['Tentatek Splattershot', 'Rapid Blaster', 'Slosher', 'Slosher', 'Splat Brella', 'Neo Splash-o-matic', 'Z+F Splat Charger', 'Z+F Splatterscope']
    self.tacticooler = ['N-ZAP \'85', 'H-3 Nozzlenose', 'Dynamo Roller', 'Snipewriter 5H', 'Dapple Dualies', 'Tri Slosher Nouveau', 'Heavy Edit Splatling']
    self.super_chump = ['N-ZAP \'89', 'Clash Blaster Neo', 'Gold Dynamo Roller', 'Inkline Tri-Stringer']
    self.kraken_royale = ['.96 Gal Deco', 'Krak-On Splat Roller', 'Bloblobber Deco']
    self.triple_splashdown = ['Custom Blaster', 'Emperry Splat Dualies']
    self.screen = ['Foil Squeezer', 'Undercover Sorella Brella']

  async def color(self, selection: str):
    if selection in self.shooter:
      return discord.Color.blue()
    
    elif selection in self.roller:
      return discord.Color.gold()

    elif selection in self.charger:
      return discord.Color.dark_magenta()
    
    elif selection in self.slosher:
      return discord.Color.darker_grey()

    elif selection in self.splatling:
      return discord.Color.purple()
    
    elif selection in self.dualies:
      return discord.Color.green()

    elif selection in self.brella:
      return discord.Color.lighter_grey()

    elif selection in self.blaster:
      return discord.Color.red()
    
    elif selection in self.brush:
      return discord.Color.teal()
    
    elif selection in self.bow:
      return discord.Color.dark_grey()
    
    elif selection in self.splatana:
      return discord.Color.orange()

  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = 'General'):
    weapon_class = weapon_class.title().strip()

    weapon_type = {'Shooter': self.shooter, 'Roller': self.roller, 'Charger': self.charger, 'Slosher': self.slosher, 'Splatling': self.splatling, 'Dualies': self.dualies, 
                  'Brella': self.brella, 'Blaster': self.blaster, 'Brush': self.brush, 'Bow': self.bow, 'Splatana': self.splatana, 'General': self.general}
    
    try:
      selection = random.choice(weapon_type[weapon_class])

    except KeyError:
      await interaction.response.send_message('Something went wrong. Maybe you misspelled something?', ephemeral = True)
    
    else:
      color = await self.color(selection)

      embed = discord.Embed(title = 'Splatoon 3 Random Weapon Line Selector', description = 'Scopes go with their respective charger kits', color = color)
      embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
      embed.add_field(name = 'Weapon Line:', value = selection)
      embed.set_footer(text = 'You can choose any weapon kit with the name above')
      await interaction.response.send_message(embed = embed, ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualies', 'Brella', 'Blaster', 'Brush', 'Bow', 'Splatana']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 3 weapon based on Sub Weapon')
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    sub_weapon = sub_weapon.title().strip()

    sub_weapons = {'Splat Bomb': self.splat_bomb, 'Suction Bomb': self.suction_bomb, 'Burst Bomb': self.burst_bomb, 'Sprinkler': self.sprinkler, 'Splash Wall': self.splash_wall, 'Fizzy Bomb': self.fizzy_bomb, 'Curling Bomb': self.curling_bomb, 
                  'Auto Bomb': self.auto_bomb, 'Squid Beakon': self.squid_beakon, 'Point Sensor': self.point_sensor, 'Ink Mine': self.ink_mine, 'Toxic Mist': self.toxic_mist, 'Angle Shooter': self.angle_shooter, 'Torpedo': self.torpedo}

    try:
      selection = random.choice(sub_weapons[sub_weapon])
    
    except KeyError:
      await interaction.response.send_message('Try again, I think you mispelled something. Don\'t forget to capitalize all words.', ephemeral = True)

    else: 
      color = await self.color(selection)

      embed = discord.Embed(title = 'Splatoon 3 Weapon Randomizer Based On Sub Weapon', color = color)
      embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
      embed.add_field(name = 'Weapon Selected!', value = selection)
      embed.set_footer(text = 'If disliked weapon, reroll')

      await interaction.response.send_message(embed = embed, ephemeral = True)

  @rss.autocomplete('sub_weapon')
  async def rss_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    subs = ['Splat Bomb', 'Suction Bomb', 'Burst Bomb', 'Sprinkler', 'Splash Wall', 'Fizzy Bomb', 'Curling Bomb', 'Auto Bomb', 'Squid Beakon', 'Point Sensor', 'Ink Mine', 'Toxic Mist', 'Angle Shooter', ' Torpedo']
    return [app_commands.Choice(name = sub_weapon, value = sub_weapon) for sub_weapon in subs if current.lower() in sub_weapon.lower()]
      
  @app_commands.command(name = 'rsp', description = 'Rolls a random Splatoon 3 weapon based on Special')
  async def rsp(self, interaction: discord.Interaction, special: str):
    special = special.title().strip()

    specials = {'Trizooka': self.trizooka, 'Big Bubbler': self.big_bubbler, 'Zipcaster': self.zipcaster, 'Tenta Missiles': self.tenta_missiles, 'Ink Storm': self.ink_storm, 'Booyah Bomb': self.booyah_bomb, 'Wave Breaker': self.wave_breaker, 
                'Ink Vac': self.ink_vac, 'Killer Wail 5.1': self.killer_wail, 'Inkjet': self.inkjet, 'Ultra Stamp': self.ultra_stamp, 'Crab Tank': self.crab_tank, 'Triple Inkstrike': self.tristrike, 'Tacticooler': self.tacticooler, 'Super Chump': self.super_chump, 'Kraken Royale': self.kraken_royale}

    try:
      selection = random.choice(specials[special])

    except KeyError:
      await interaction.response.send_message('Try again, maybe there was a typo somewhere', ephemeral = True)

    else:
      color = await self.color(selection)

      embed = discord.Embed(title = 'Splatoon 3 Weapon Randomizer Based On Special', description = f'{special} go brrr', color = color)
      embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
      embed.add_field(name = 'Weapon Selected!', value = selection)
      embed.set_footer(text = 'If disliked weapon, reroll')
      
      await interaction.response.send_message(embed = embed, ephemeral = True)
  
  @rsp.autocomplete('special')
  async def rsp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    specials = ['Trizooka', 'Big Bubbler', 'Zipcaster', 'Tenta Missiles, Ink Storm', 'Booyah Bomb', 'Wave Breaker', 'Ink Vac', 'Killer Wail 5.1', 'Inkjet', 'Ultra Stamp', 'Crab Tank', 'Triple Inkstrike', 'Tacticooler', 'Super Chump', 'Kraken Royale']
    return [app_commands.Choice(name = special, value = special) for special in specials if current.lower() in special.lower()]
  

async def setup(bot: commands.Bot):
  await bot.add_cog(Splat2nRandomWeapon(bot), guild = None)