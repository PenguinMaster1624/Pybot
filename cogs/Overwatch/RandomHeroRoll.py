from orm_models import Session, OWHeroes, OWRoles, OWSubroles
from discord import app_commands
from discord.ext import commands
from sqlalchemy import select
from io import BytesIO
import discord
import random


class OverwatchRandomHero(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def color(self, selection: str) -> discord.Color:
        match selection:
            case 'Tank':
                return discord.Color.blue()
        
            case 'Damage':
                return discord.Color.red()
        
            case 'Support':
                return discord.Color.gold()
        
    @app_commands.command(name = 'ow_hero', description = 'Rolls a hero for you in Overwatch 2')
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ow_hero(self, interaction: discord.Interaction, role: str = None) -> None:
        stmt = select(OWRoles.name)
        with Session.begin() as session:
            roles = session.scalars(stmt)

        if role is not None:
            role = role.title().strip()

            if role in roles:
                command = select(OWHeroes).join(OWRoles, OWHeroes.role_id == OWRoles.id).where(OWHeroes.role.has(OWRoles.name == role))

            else:
                await interaction.response.send_message(f'{role} is not a valid role in Overwatch', ephemeral = True)
        else:
            command = select(OWHeroes).join(OWRoles, OWHeroes.role_id == OWRoles.id)
 
        with Session.begin() as session:
            heroes = session.scalars(command).all()
            selection = random.choice(heroes)
            
            image_bytes = [BytesIO(selection.image), BytesIO(selection.role.image), BytesIO(selection.subrole.image)]

            names = ['portrait.png', 'role.png', 'subrole.png']
            files = []
            for index, image in enumerate(image_bytes):
                files.append(discord.File(image, filename=names[index]))

            color = await self.color(selection.role.name)
            embed = discord.Embed(title = selection.name, description = selection.description, color = color)
            embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
            embed.set_thumbnail(url = 'attachment://role.png')
            embed.set_image(url = 'attachment://portrait.png')
            embed.set_footer(text = f'{selection.subrole.name} - {selection.subrole.passive}', icon_url = 'attachment://subrole.png')

        await interaction.response.send_message(embed = embed, files=files, ephemeral = True)
        
    @ow_hero.autocomplete('role')
    async def ow_hero_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        roles = ['Tank', 'Damage', 'Support']
        return [app_commands.Choice(name = role, value = role) for role in roles if current.lower() in role.lower()]

async def setup(bot: commands.Bot):
  await bot.add_cog(OverwatchRandomHero(bot))