from orm_models import Session, MK8DXTracks, MK8DXCups
from discord.ext import commands
from discord import app_commands
from sqlalchemy import select
from io import BytesIO
import discord
import random


class MK8Map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'mk8m', description = 'Rolls a random map from the available Mario Kart 8 Deluxe maps, includes DLC')
  async def mk8m(self, interaction: discord.Interaction, cup: str = None):
    stmt = select(MK8DXCups.name)
    with Session.begin() as session:
      cups = session.scalars(stmt)

    if cup is not None:
      cup = cup.title().strip()
      if cup in cups:
        command = select(MK8DXTracks).join(MK8DXCups, MK8DXTracks.cup_id == MK8DXCups.id).where(MK8DXCups.name == cup)

      else:
        await interaction.response.send_message(f'{cup} Cup is not a valid Mario Kart cup', ephemeral = True)
        return
    
    else:
      command = select(MK8DXTracks).join(MK8DXCups, MK8DXTracks.cup_id == MK8DXCups.id)

    embed = discord.Embed(title = 'Mario Kart 8 Deluxe Map Selector', color = discord.Color.random())

    with Session.begin() as session:
      courses = session.scalars(command).all()
      course = random.choice(courses)

      course_image = BytesIO(course.image)
      cup_image = BytesIO(course.cup.image)

      files = [discord.File(course_image, 'track.png'), discord.File(cup_image, 'cup.png')]
      embed.add_field(name = course.name, value = '\u200b')
      embed.set_footer(text = f'Found in the {course.cup.name} Cup')

    embed.set_thumbnail(url = 'attachment://cup.png')
    embed.set_image(url = 'attachment://track.png')
    embed.set_author(name = interaction.user.display_name, icon_url=interaction.user.display_avatar)
    
    await interaction.response.send_message(embed = embed, files = files, ephemeral = True)


  @mk8m.autocomplete('cup')
  async def mk8m_autocomplete(self, interaction: discord.Interaction, current: str)-> list[app_commands.Choice[str]]:
    cups = ['Mushroom', 'Flower', 'Star', 'Special', 'Shell', 'Banana', 'Leaf', 'Lightning', 'Egg', 'Crossing', 'Triforce', 'Bell', 'Golden Dash', 'Lucky Cat', 'Turnip', 'Propeller', 'Rock', 'Moon', 'Fruit', 'Boomerang', 'Feather', 'Cherry', 'Acorn', 'Spiny']
    return [app_commands.Choice(name = cup, value = cup) for cup in cups if current.lower() in cup.lower()]

async def setup(bot: commands.Bot):
  await bot.add_cog(MK8Map(bot))