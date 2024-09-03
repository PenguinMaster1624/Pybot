from discord import app_commands
from discord.ext import commands
import discord, random, sqlite3

class OverwatchRandomHero(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def db_connect(self, command: str, role: tuple[str | None]) -> list[tuple[str]]:
        with sqlite3.connect('Utils/Game Stuff.db') as db:
          cursor = db.cursor()
          if all(role):
            return [course for course in cursor.execute(command, role)]

          else:
            return [course for course in cursor.execute(command)]

    async def color(self, selection: str):
        tank = [hero[1] for hero in await self.db_connect('SELECT * FROM "Overwatch 2 Heroes" WHERE Role = ?', ('Tank',))]
        dps = [hero[1] for hero in await self.db_connect('SELECT * FROM "Overwatch 2 Heroes" WHERE Role = ?', ('DPS',))]
        support = [hero[1] for hero in await self.db_connect('SELECT * FROM "Overwatch 2 Heroes" WHERE Role = ?', ('Support',))]
        
        if selection in tank:
            return discord.Color.blue()
        
        elif selection in dps:
            return discord.Color.red()
        
        elif selection in support:
            return discord.Color.gold()
    
    async def embed_setup(self, interaction: discord.Interaction, selection: tuple[str]) -> discord.Embed:
        color = await self.color(selection[0])
        embed = discord.Embed(title = 'Overwatch 2 Character Randomizer', description = f'Enjoy playing a game with the following {selection[1]} character! :)', color = color)
        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
        embed.add_field(name = 'You got...', value = f'**{selection[0]}**! Hope you enjoy!')
        embed.set_footer(text = 'If you don\'t wanna play this character, reroll by using the command again')

        return embed
        
    @app_commands.command(name = 'ow_hero', description = 'Rolls a hero for you in Overwatch 2')
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ow_hero(self, interaction: discord.Interaction, role: str = None) -> None:

        if role is not None:
            role = role.title().strip()
            if role.upper() == 'DPS':
                role = role.upper()

            if role in ['Tank', 'DPS', 'Support']:
                command = 'SELECT Hero, Role FROM "Overwatch 2 Heroes" WHERE Role = ?'

            else:
                await interaction.response.send_message(f'{role} is not a valid role in Overwatch 2', ephemeral = True)
        else:
            command = 'SELECT Hero, Role FROM "Overwatch 2 Heroes"'

        heroes = await self.db_connect(command = command, role = (role,))
        selection = random.choice(heroes)

        embed = await self.embed_setup(interaction = interaction, selection = selection)
        await interaction.response.send_message(embed = embed, ephemeral = True)
        
    @ow_hero.autocomplete('role')
    async def ow_hero_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        roles = ['Tank', 'DPS', 'Support']
        return [app_commands.Choice(name = role, value = role) for role in roles if current.lower() in role.lower()]

async def setup(bot: commands.Bot):
  await bot.add_cog(OverwatchRandomHero(bot))