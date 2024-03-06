from discord.ext import commands
from discord import app_commands
import random, discord, sqlite3, re

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.db_path = 'cogs/Splatoon/SplatoonUtils/Splatoon 3.db'

  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = None):
    if weapon_class is not None:
      weapon_class = weapon_class.title().strip()
      search = re.search('^Shooter$|^Roller$|^Charger$|^Slosher$|^Splatling$|^Dualies$|^Brella$|^Blaster$|^Brush$|^Stringer$|^Splatana$', weapon_class)
      if search:
        command = f'SELECT Main, Introduced FROM Weapons WHERE Class = "{weapon_class}"'
      
      else:
        await interaction.response.send_message(f'{weapon_class} is not a valid weapon class', ephemeral = True)
    
    else:
      command = 'SELECT Main, Introduced FROM Weapons'

    with sqlite3.connect(self.db_path) as db:
      cursor = db.cursor()
      weapons = [weapon for weapon in cursor.execute(command)]

    selection = random.choice(weapons)

    embed = discord.Embed(title = 'Splatoon 3 Random Weapon Selector', color = discord.Color.blue())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.add_field(name = 'The Council Has Decided Your Fate!', value = selection[0])
    embed.set_footer(text = f'Introduced In {selection[1]}')
    
    await interaction.response.send_message(embed = embed, ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualies', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 3 weapon based on Sub Weapon')
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    sub_weapon = sub_weapon.title().strip()
    search = re.search('^Splat Bomb$|^Suction Bomb$|^Burst Bomb$|^Splash Wall$|^Fizzy Bomb$|^Curling Bomb$|^Auto Bomb$|^Squid Beakon$|^Point Sensor$|^Ink Mine$|^Toxic Mist$|^Angle Shooter$|^Torpedo$', sub_weapon)
    if not search:
      await interaction.response.send_message('That is not a valid sub weapon', ephemeral = True)
      return
      
    with sqlite3.connect(self.db_path) as db:
      cursor = db.cursor()
      weapons = [weapon for weapon in cursor.execute(f'SELECT Main, Introduced FROM Weapons WHERE Sub = "{sub_weapon}"')]

    selection = random.choice(weapons)

    embed = discord.Embed(title = 'Splatoon 3 Weapon Randomizer Based On Sub Weapon', color = discord.Color.blurple())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.add_field(name = 'The Council Has Decided Your Fate!', value = selection[0])
    embed.set_footer(text = f'Introduced In {selection[1]}')

    await interaction.response.send_message(embed = embed, ephemeral = True)

  @rss.autocomplete('sub_weapon')
  async def rss_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    subs = ['Splat Bomb', 'Suction Bomb', 'Burst Bomb', 'Sprinkler', 'Splash Wall', 'Fizzy Bomb', 'Curling Bomb', 'Auto Bomb', 'Squid Beakon', 'Point Sensor', 'Ink Mine', 'Toxic Mist', 'Angle Shooter', 'Torpedo']
    return [app_commands.Choice(name = sub_weapon, value = sub_weapon) for sub_weapon in subs if current.lower() in sub_weapon.lower()]
      
  @app_commands.command(name = 'rsp', description = 'Rolls a random Splatoon 3 weapon based on Special')
  async def rsp(self, interaction: discord.Interaction, special: str):
    special = special.title().strip()
    search = re.search('^Trizooka$|^Big Bubbler$|^Zipcaster$|^Tenta Missiles$|^Ink Storm$|^Booyah Bomb$|^Wave Breaker$|^Ink Vac$|^Killer Wail 5.1$|^Inkjet$|^Ultra Stamp$|^Crab Tank$|^Triple Inkstrike$|^Tacticooler$|^Super Chump$|^Kraken Royale$', special)
    if not search:
      await interaction.response.send_message('That is not a valid special', ephemeral = True)
      return
    
    with sqlite3.connect(self.db_path) as db:
      cursor = db.cursor()
      weapons = [weapon for weapon in cursor.execute(f'SELECT Main, Introduced FROM Weapons WHERE Special = "{special}"')]

      selection = random.choice(weapons)


    embed = discord.Embed(title = 'Splatoon 3 Weapon Randomizer Based On Special', description = f'{special} go brrr', color = discord.Color.purple())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.add_field(name = 'The Council Has Decided Your Fate!', value = selection[0])
    embed.set_footer(text = f'Introduced In {selection[1]}')

    await interaction.response.send_message(embed = embed, ephemeral = True)
  
  @rsp.autocomplete('special')
  async def rsp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    specials = ['Trizooka', 'Big Bubbler', 'Zipcaster', 'Tenta Missiles', 'Ink Storm', 'Booyah Bomb', 'Wave Breaker', 'Ink Vac', 'Killer Wail 5.1', 'Inkjet', 'Ultra Stamp', 'Crab Tank', 'Triple Inkstrike', 'Tacticooler', 'Super Chump', 'Kraken Royale']
    return [app_commands.Choice(name = special, value = special) for special in specials if current.lower() in special.lower()]
  

async def setup(bot: commands.Bot):
  await bot.add_cog(Splat2nRandomWeapon(bot), guild = None)