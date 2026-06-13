from orm_models import Session, S3Kits, S3Subs, S3Specials, S3Classes
from discord import app_commands
from discord.ext import commands
from sqlalchemy import select
from io import BytesIO
from PIL import Image
import discord
import random



class Splatoon3RandomWeapon(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot


  async def kit_image(self, selection: S3Kits) -> discord.File:
    with Session.begin() as session:
      selection = session.merge(selection)
      main = BytesIO(selection.image)
      sub = BytesIO(selection.sub.image)
      special = BytesIO(selection.special.image)

    final = BytesIO()
    
    image_main = Image.open(main)
    image_sub = Image.open(sub).resize((image_main.width//2, image_main.height//2))
    image_special = Image.open(special).resize((image_main.width//2, image_main.height//2))

    merged = Image.new('RGBA', (image_main.width, image_main.height + image_main.height//2))
    merged.paste(image_main, (0, 0))
    merged.paste(image_sub, (0, image_main.height))
    merged.paste(image_special, (image_sub.width, image_main.height))

    merged.save(final, 'PNG')
    final.seek(0)

    return discord.File(fp=final, filename=f'kit.png')
    
  async def get_class_image(self, weapon_class: S3Classes) -> discord.File:
    image = BytesIO(weapon_class.image)
    return discord.File(fp=image, filename='class.png')
  
  async def setup_embed(self, interaction: discord.Interaction, selection: S3Kits) -> discord.Embed:
    embed = discord.Embed(title = 'Splatoon 3 Random Weapon Selector', color = discord.Color.blue())
    embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
    embed.set_image(url='attachment://kit.png')
    embed.set_thumbnail(url='attachment://class.png')

    with Session.begin() as session:
      selection = session.merge(selection)
      embed.add_field(name = f'{selection.main} - {selection.points_for_special}p', value = f'{selection.sub.name} Tank Consumption - {selection.sub.ink_consumption}%')
      embed.set_footer(text = f'Introduced In {selection.introduced}')

    return embed

  @app_commands.command(name = 'rsw', description = 'Rolls a random Splatoon 3 weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rsw(self, interaction: discord.Interaction, weapon_class: str = None):
    stmt = select(S3Classes.name)
    with Session.begin() as session:
      classes = session.scalars(stmt)

    if weapon_class is not None:
      weapon_class = weapon_class.title().strip()
      if weapon_class in classes:
        command = select(S3Kits).join(S3Kits.sub).join(S3Kits.special).join(S3Kits.s3_class).where(S3Classes.name == weapon_class)

      else:
        await interaction.response.send_message(f'{weapon_class} is not a valid weapon class', ephemeral = True)

    else:
      command = select(S3Kits).join(S3Kits.sub).join(S3Kits.special).join(S3Kits.s3_class)

    with Session.begin() as session:
      weapons = session.execute(command).scalars().all()
      
      selection = random.choice(weapons)
      image = BytesIO(selection.s3_class.image)
    
    class_image = discord.File(fp=image, filename='class.png')
    kit_image = await self.kit_image(selection)

    embed = await self.setup_embed(interaction, selection)
    await interaction.response.send_message(embed = embed, files = [class_image, kit_image], ephemeral = True)

  @rsw.autocomplete('weapon_class')
  async def rsw_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    classes = ['Shooter', 'Roller', 'Charger', 'Slosher', 'Splatling', 'Dualie', 'Brella', 'Blaster', 'Brush', 'Stringer', 'Splatana']
    return [app_commands.Choice(name = Class, value = Class) for Class in classes if current.lower() in Class.lower()]

  @app_commands.command(name = 'rss', description = 'Rolls a random Splatoon 3 weapon based on Sub Weapon')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rss(self, interaction: discord.Interaction, sub_weapon: str):
    sub_weapon = sub_weapon.title().strip()
    stmt = select(S3Subs.name)
    with Session.begin() as session:
      subs = session.scalars(stmt)

    if sub_weapon not in subs:
      await interaction.response.send_message('That is not a valid sub weapon', ephemeral = True)
      return

    command = select(S3Kits).join(S3Kits.sub).join(S3Kits.special).join(S3Kits.s3_class).where(S3Subs.name == sub_weapon)
    
    with Session.begin() as session:
      weapons = session.execute(command).scalars().all()
      
      selection = random.choice(weapons)
      image = BytesIO(selection.s3_class.image)
    
    class_image = discord.File(fp=image, filename='class.png')
    kit_image = await self.kit_image(selection)

    embed = await self.setup_embed(interaction, selection)
    await interaction.response.send_message(embed = embed, files = [class_image, kit_image], ephemeral = True)

  @rss.autocomplete('sub_weapon')
  async def rss_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    subs = ['Splat Bomb', 'Suction Bomb', 'Burst Bomb', 'Sprinkler', 'Splash Wall', 'Fizzy Bomb', 'Curling Bomb', 'Auto Bomb', 'Squid Beakon', 'Point Sensor', 'Ink Mine', 'Toxic Mist', 'Angle Shooter', 'Torpedo']
    return [app_commands.Choice(name = sub_weapon, value = sub_weapon) for sub_weapon in subs if current.lower() in sub_weapon.lower()]

  @app_commands.command(name = 'rsp', description = 'Rolls a random Splatoon 3 weapon based on Special')
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  async def rsp(self, interaction: discord.Interaction, special: str):
    special = special.title().strip()
    stmt = select(S3Specials.name)
    with Session.begin() as session:
      specials = session.scalars(stmt)

    if special not in specials:
      await interaction.response.send_message('That is not a valid special weapon', ephemeral = True)
      return

    command = select(S3Kits).join(S3Kits.sub).join(S3Kits.special).join(S3Kits.s3_class).where(S3Specials.name == special)
    
    with Session.begin() as session:
      weapons = session.execute(command).scalars().all()
      
      selection = random.choice(weapons)
      image = BytesIO(selection.s3_class.image)
    
    class_image = discord.File(fp=image, filename='class.png')
    kit_image = await self.kit_image(selection)

    embed = await self.setup_embed(interaction, selection)
    await interaction.response.send_message(embed = embed, files = [class_image, kit_image], ephemeral = True)

  @rsp.autocomplete('special')
  async def rsp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    specials = ['Trizooka', 'Big Bubbler', 'Zipcaster', 'Tenta Missiles', 'Ink Storm', 'Booyah Bomb', 'Wave Breaker', 'Ink Vac', 'Killer Wail 5.1', 'Inkjet', 'Ultra Stamp', 'Crab Tank', 'Triple Inkstrike', 'Tacticooler', 'Super Chump', 'Kraken Royale']
    return [app_commands.Choice(name = special, value = special) for special in specials if current.lower() in special.lower()]


async def setup(bot: commands.Bot):
  await bot.add_cog(Splatoon3RandomWeapon(bot), guild = None)
