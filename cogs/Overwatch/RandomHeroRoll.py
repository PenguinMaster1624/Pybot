from discord import app_commands
from discord.ext import commands
import discord, random

class OverwatchRandomHero(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tank = ['D.va', 'Doomfist', 'Junker Queen', 'Orisa', 'Ramattra', 'Reinhardt', 'Roadhog', 'Sigma', 'Winston', 'Wrecking Ball', 'Zarya']
        self.dps = ['Ashe', 'Bastion', 'Cassidy', 'Echo', 'Genji', 'Hanzo', 'Junkrat', 'Mei', 'Pharah', 'Reaper', 'Sojourn', 'Soldier: 76', 'Sombra', 'Symmetra', 'Torbjörn', 'Tracer', 'Widowmaker']
        self.support = ['Ana', 'Baptiste', 'Brigitte', 'Kiriko', 'Lúcio', 'Lifeweaver', 'Mercy', 'Moira', 'Zenyatta']
        self.all = list(self.tank + self.dps + self.support)

        self.role_names = ['Tank', 'DPS', 'Support']

    async def color(self, selection: str):
        if selection in self.tank:
            return discord.Color.blue()
        
        elif selection in self.dps:
            return discord.Color.red()
        
        elif selection in self.support:
            return discord.Color.gold()
        
    async def embed_setup(self, interaction: discord.Interaction, selection: str):
        color = await self.color(selection)
        embed = discord.Embed(title = 'Overwatch 2 Character Randomizer', description = 'Enjoy playing a game with the following character! :)', color = color)
        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
        embed.add_field(name = 'You got...', value = f'**{selection}**! Hope you enjoy!')
        embed.set_footer(text = 'If you don\'t wanna play this character, reroll by using the command again')

        return embed
        
    @app_commands.command(name = 'ow_hero', description = 'Rolls a hero for you in Overwatch 2')
    async def ow_hero(self, interaction: discord.Interaction, role: str = None):
        roles = {'Tank': self.tank, 'DPS': self.dps, 'Support': self.support}

        if role != None:
            for i in self.role_names:
                if role.title().strip() == i:
                    selection = random.choice(roles[role.title().strip()])
                    embed = await self.embed_setup(interaction = interaction, selection = selection)

                elif role.upper().strip() == i:
                    selection = random.choice(roles[role.upper().strip()])
                    embed = await self.embed_setup(interaction = interaction, selection = selection)
                
        else:
            randomized_role = random.choice(self.role_names)
            selection = random.choice(roles[randomized_role])
            embed = await self.embed_setup(interaction = interaction, selection = selection)

        try:
            await interaction.response.send_message(embed = embed, ephemeral = True)
        
        except UnboundLocalError:
            await interaction.response.send_message(content = 'String not recognized', ephemeral = True)
        
    @ow_hero.autocomplete('role')
    async def ow_hero_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        roles = ['Tank', 'DPS', 'Support']
        return [app_commands.Choice(name = role, value = role) for role in roles if current.lower() in role.lower()]

async def setup(bot: commands.Bot):
  await bot.add_cog(OverwatchRandomHero(bot))