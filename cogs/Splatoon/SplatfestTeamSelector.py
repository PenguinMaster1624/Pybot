from models import FestivalsResponse, Votes
from discord import app_commands, User
from utils.sessions import fetch_data
from discord.ext import commands
import discord

class SplatfestButtons(discord.ui.View):
    def __init__(self, embed: discord.Embed, bot: commands.Bot) -> None:
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed


    async def setup(self) -> None:
        self.model = await fetch_data(url='https://splatoon3.ink/data/festivals.json', model=FestivalsResponse)
        self.votes = [Votes(team_name=team.name) for team in self.model.teams]

    async def player_check(self, member: User, team: str) -> str | None:
        for teams in self.votes:
            if team == teams.team_name and member in teams.members:
                return 'You\'re already on that team, you can\'t vote for the same team you\'re repping!'
            
            elif team != teams.team_name and member in teams.members:
                teams.members.remove(member)
            
            else:
                teams.members.append(member)

    async def embed_setup(self) -> discord.Embed:
        for num in range(len(self.children)):
            self.children[num].label = f'{self.votes[num].team_name}: {len(self.votes[num].members)}'

        for index in range(len(self.votes)):
            player_list = f'\n'.join(self.votes[index].members)
            self.embed.set_field_at(index=index, name=self.votes[index].team_name, value= player_list if player_list else None)

    async def embed_change(self, interaction: discord.Interaction, helper: str | None) -> None:
        if interaction.response.is_done() is False and helper is not None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            await self.embed_setup()
            await interaction.response.edit_message(embed = self.embed, view = self)

    @discord.ui.button(label = 'Shiver', style = discord.ButtonStyle.blurple)
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):
        helper = await self.player_check(member=interaction.user, team = self.model.teams[0].name)

        await self.embed_change(interaction=interaction, helper=helper)

    @discord.ui.button(label = 'Frye', style = discord.ButtonStyle.red)
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):
        helper = await self.player_check(member=interaction.user, team=self.model.teams[1].name)

        await self.embed_change(interaction=interaction, helper=helper)

    @discord.ui.button(label = 'Big Man', style = discord.ButtonStyle.green)
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
        helper = await self.player_check(member=interaction.user, team = self.model.teams[2].name)

        await self.embed_change(interaction=interaction, helper=helper)

class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def SplatfestTeams(self, interaction: discord.Interaction):
        model = await fetch_data(url='https://splatoon3.ink/data/festivals.json', model=FestivalsResponse)
        print(model)
        if await self.bot.is_owner(interaction.user) is False:
            await interaction.response.send_message(content = 'You need to be the bot owner to use this command', ephemeral = True)
            return
        
        elif model.is_votable is False:
            await interaction.response.send_message('No Splatfest soon', ephemeral = True)
            return
    
        start = int(model.start)
        end = int(model.end)

        embed = discord.Embed(title = model.title, description = f"Start Time: <t:{start}:t>,<t:{start}:R>\nEnd TIme: <t:{end}:t>, <t:{end}:R>", color=discord.Color.orange())
        for i in range(3):
            embed.add_field(name = model.teams[i].name, value = model.teams[i].name, inline = True)
        
        embed.set_image(url = model.image_url)
        embed.set_footer(text = 'Happy Splatting :)')

        await interaction.response.send_message(embed = embed, view = SplatfestButtons(embed=embed, bot=self.bot))

async def setup(bot: commands.Bot):
    await bot.add_cog(SplatfestTeamChoices(bot))