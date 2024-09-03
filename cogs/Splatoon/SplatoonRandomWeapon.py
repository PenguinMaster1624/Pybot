from discord.ext import commands
from discord import app_commands
import random, discord, sqlite3

class Splatoon3RandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.db_path = 'Utils/Game Stuff.db'

  async def db_connect(self, command: str, select: tuple[str | None]) -> list[tuple[str]]:
    with sqlite3.connect(self.db_path) as db:
      cursor = db.cursor()
      if all(select):
        return [weapon for weapon in cursor.execute(command, select)]

      else:
        return [weapon for weapon in cursor.execute(command)]


  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = None):
    if weapon_class is not None:
      weapon_class = weapon_class.title().strip()
      if weapon_class in ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualies', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']:
        command = 'SELECT Main, Class, Introduced FROM "Splatoon 3 Weapons" WHERE Class = ?'
      
      else:
        await interaction.response.send_message(f'{weapon_class} is not a valid weapon class', ephemeral = True)
    
    else:
      command = 'SELECT Main, Class, Introduced FROM "Splatoon 3 Weapons"'

    weapons = await self.db_connect(command = command, select = (weapon_class,))
    selection = random.choice(weapons)

    embed = discord.Embed(title = 'Splatoon 3 Random Weapon Selector', color = discord.Color.blue())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.add_field(name = 'The Council Has Decided Your Fate!', value = selection[0])
    embed.set_footer(text = f'Introduced In {selection[2]}')
    
    await interaction.response.send_message(embed = embed, ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualies', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 3 weapon based on Sub Weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    sub_weapon = sub_weapon.title().strip()
    if not sub_weapon in ['Splat Bomb', 'Suction Bomb', 'Burst Bomb', 'Sprinkler', 'Splash Wall', 'Fizzy Bomb', 'Curling Bomb', 'Auto Bomb', 'Squid Beakon', 'Point Sensor', 'Ink Mine', 'Toxic Mist', 'Angle Shooter', 'Torpedo']:
      await interaction.response.send_message('That is not a valid sub weapon', ephemeral = True)
      return
      
    weapons = await self.db_connect(command = 'SELECT Main, Introduced FROM "Splatoon 3 Weapons" WHERE Sub = ?', select = (sub_weapon,))

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
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rsp(self, interaction: discord.Interaction, special: str):
    special = special.title().strip()
    if not special in ['Trizooka', 'Big Bubbler', 'Zipcaster', 'Tenta Missiles', 'Ink Storm', 'Booyah Bomb', 'Wave Breaker', 'Ink Vac', 'Killer Wail 5.1', 'Inkjet', 'Ultra Stamp', 'Crab Tank', 'Triple Inkstrike', 'Tacticooler', 'Super Chump', 'Kraken Royale']:
      await interaction.response.send_message('That is not a valid special', ephemeral = True)
      return
    
    weapons = await self.db_connect(command = 'SELECT Main, Introduced FROM "Splatoon 3 Weapons" WHERE Special = ?', select = (special,))
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
  await bot.add_cog(Splatoon3RandomWeapon(bot), guild = None)