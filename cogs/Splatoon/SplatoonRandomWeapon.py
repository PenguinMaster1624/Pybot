from discord.ext import commands
from discord import app_commands
import random, discord, sqlite3
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests


class Splatoon3RandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.db_path = 'Utils/Game Stuff.db'

  async def db_connect(self, command: str, select: tuple[str | None]) -> list[tuple[str]]:
    with sqlite3.connect(self.db_path) as db:
      cursor = db.cursor()
      if all(select):
        return list(cursor.execute(command, select))

      else:
        return list(cursor.execute(command))

  async def get_source(self, selection: tuple[str]) -> discord.File:
    images = []

    for weapon, weapon_type in zip(range(3), ['Main', 'Sub', 'Special']):
      weapon_name = selection[weapon].replace(' ', '_')

      match weapon_type:
          case 'Main':
              url = f'https://splatoonwiki.org/wiki/File:S3_Weapon_Main_{weapon_name}_2D_Current.png'
              
          case 'Sub':
              url = f'https://splatoonwiki.org/wiki/File:S3_Weapon_Sub_{weapon_name}_Flat.png'

          case 'Special':
              url = f'https://splatoonwiki.org/wiki/File:S3_Weapon_Special_{weapon_name}.png'

          case _:
              return 'https://splatoonwiki.org/wiki/File:S2_Salmon_Run_question_mark_capsule.png'
         

      with requests.get(url) as response:
          soup = BeautifulSoup(response.content, 'html5lib')
          image = BytesIO(requests.get(f"https:{soup.find_all('img', alt=True, src=True)[0]['src']}").content)
          image.seek(0)
          images.append(image)

    final = BytesIO()
    
    image_main = Image.open(images[0])
    image_sub = Image.open(images[1]).resize((image_main.width//2, image_main.height//2))
    image_special = Image.open(images[2]).resize((image_main.width//2, image_main.height//2))

    merged = Image.new('RGBA', (image_main.width, image_main.height + image_main.height//2))
    merged.paste(image_main, (0, 0))
    merged.paste(image_sub, (0, image_main.height))
    merged.paste(image_special, (image_sub.width, image_main.height))

    merged.save(final, 'PNG')
    final.seek(0)

    return discord.File(fp=final, filename=f'kit.png')
    
  async def setup_embed(self, interaction: discord.Interaction, selection: tuple[str]) -> discord.Embed:
    embed = discord.Embed(title = 'Splatoon 3 Random Weapon Selector', color = discord.Color.blue())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.add_field(name = 'The Council Has Decided Your Fate!', value = selection[0])
    embed.set_image(url='attachment://kit.png')
    embed.set_thumbnail(url='attachment://class.png')
    embed.set_footer(text = f'Introduced In {selection[4]}')

    return embed
    
  async def get_class_image(self, weapon_class: str) -> discord.File:
    weapon_class = weapon_class.title().strip()
    if weapon_class in ['Blaster', 'Slosher']:
        weapon_class = f'{weapon_class} (weapon class)'

    with requests.get('https://splatoonwiki.org/wiki/List_of_main_weapons_in_Splatoon_3') as response:
        soup = BeautifulSoup(response.content, 'html5lib')
        source = soup.find('a', title=weapon_class)
        
        image = BytesIO(requests.get(f"https:{source.find('img')['src']}").content)
        return discord.File(fp=image, filename='class.png')
        

  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = None):
    if weapon_class is not None:
      weapon_class = weapon_class.title().strip()
      if weapon_class in ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualie', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']:
        command = 'SELECT Main, Sub, Special, Class, Introduced FROM "Splatoon 3 Weapons" WHERE Class = ?'
      
      else:
        await interaction.response.send_message(f'{weapon_class} is not a valid weapon class', ephemeral = True)
    
    else:
      command = 'SELECT Main, Sub, Special, Class, Introduced FROM "Splatoon 3 Weapons"'

    await interaction.response.defer(ephemeral=True, thinking=True)
    weapons = await self.db_connect(command = command, select = (weapon_class,))
    selection = random.choice(weapons)

    class_image = await self.get_class_image(selection[3])
    kit_image = await self.get_source(selection)

    embed = await self.setup_embed(interaction, selection)
    
    await interaction.followup.send(embed = embed, files = [class_image, kit_image], ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualie', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 3 weapon based on Sub Weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    sub_weapon = sub_weapon.title().strip()
    if not sub_weapon in ['Splat Bomb', 'Suction Bomb', 'Burst Bomb', 'Sprinkler', 'Splash Wall', 'Fizzy Bomb', 'Curling Bomb', 'Auto Bomb', 'Squid Beakon', 'Point Sensor', 'Ink Mine', 'Toxic Mist', 'Angle Shooter', 'Torpedo']:
      await interaction.response.send_message('That is not a valid sub weapon', ephemeral = True)
      return
      
    await interaction.response.defer(ephemeral=True, thinking=True)
    weapons = await self.db_connect(command = 'SELECT Main, Sub, Special, Class, Introduced FROM "Splatoon 3 Weapons" WHERE Sub = ?', select = (sub_weapon,))
    selection = random.choice(weapons)

    class_image = await self.get_class_image(selection[3])
    kit_image = await self.get_source(selection)

    embed = await self.setup_embed(interaction, selection)
    await interaction.followup.send(embed = embed, files = [class_image, kit_image], ephemeral = True)

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
    
    await interaction.response.defer(ephemeral=True, thinking=True)
    weapons = await self.db_connect(command = 'SELECT Main, Sub, Special, Class, Introduced FROM "Splatoon 3 Weapons" WHERE Special = ?', select = (special,))
    selection = random.choice(weapons)

    class_image = await self.get_class_image(selection[3])
    kit_image = await self.get_source(selection)

    embed = await self.setup_embed(interaction, selection)

    await interaction.followup.send(embed = embed, files = [class_image, kit_image], ephemeral = True)
  
  @rsp.autocomplete('special')
  async def rsp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    specials = ['Trizooka', 'Big Bubbler', 'Zipcaster', 'Tenta Missiles', 'Ink Storm', 'Booyah Bomb', 'Wave Breaker', 'Ink Vac', 'Killer Wail 5.1', 'Inkjet', 'Ultra Stamp', 'Crab Tank', 'Triple Inkstrike', 'Tacticooler', 'Super Chump', 'Kraken Royale']
    return [app_commands.Choice(name = special, value = special) for special in specials if current.lower() in special.lower()]
  

async def setup(bot: commands.Bot):
  await bot.add_cog(Splatoon3RandomWeapon(bot), guild = None)