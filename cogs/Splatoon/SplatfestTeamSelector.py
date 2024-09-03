from .SplatoonUtils.SplatoonUtils import generate_timestamp
from discord import app_commands
from discord.ext import commands
import discord, requests


def fetch_data() -> dict:
    with requests.get('https://splatoon3.ink/data/festivals.json') as response:
        js = response.json()
        return js['US']['data']['festRecords']['nodes'][0]
        
def team_names() -> list[str]:
    data = fetch_data()
    return [data['teams'][i]['teamName'] for i in range(3)]

teams = team_names()

class SplatfestButtons(discord.ui.View):
    def __init__(self, embed: discord.Embed) -> None:
        super().__init__(timeout = None)
        self.embed = embed

        self.total = {
            'Shiver': [],
            'Frye': [],
            'Big Man': []
        }


    async def player_check(self, user_name: str, team: str) -> str | None:
        for person, players in self.total.items():
            if person != team:
                if user_name in players:
                    players.remove(user_name)
            
            elif person == team and user_name in players:
                return 'You\'re already on that team, you can\'t vote for the same team you\'re repping!'
                
            else:
                players.append(user_name)

    async def embed_setup(self) -> discord.Embed:
        players = list(self.total.values())
        for num in range(len(self.children)):
            self.children[num].label = f'{teams[num]}: {len(players[num])}'

        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            self.embed.set_field_at(index=j, name = teams[j], value = player_list if player_list else None)

    async def embed_change(self, interaction: discord.Interaction, helper: str | None) -> None:
        if interaction.response.is_done() is False and helper is not None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            await self.embed_setup()
            await interaction.response.edit_message(embed = self.embed, view = self)

    @discord.ui.button(label = teams[0], style = discord.ButtonStyle.blurple, custom_id = 'Shiver')
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Shiver')

        await self.embed_change(interaction=interaction, helper=helper)

    @discord.ui.button(label = teams[1], style = discord.ButtonStyle.red)
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Frye')

        await self.embed_change(interaction=interaction, helper=helper)

    @discord.ui.button(label = teams[2], style = discord.ButtonStyle.green)
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Big Man')

        await self.embed_change(interaction=interaction, helper=helper)

class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def SplatfestTeams(self, interaction: discord.Interaction):
        data = fetch_data()
        if await self.bot.is_owner(interaction.user) is False:
            await interaction.response.send_message(content = 'You need to be the bot owner to use this command', ephemeral = True)
            return
        
        elif data['isVotable'] is False:
            await interaction.response.send_message('No Splatfest soon', ephemeral = True)
            return
    
        start_time = await generate_timestamp(time=data['startTime'])
        end_time = await generate_timestamp(time=data['endTime'])
        embed = discord.Embed(title = data['title'], description = f"Start Time: <t:{start_time}:t>,<t:{start_time}:R>\nEnd TIme: <t:{end_time}:t>, <t:{end_time}:R>", color=discord.Color.orange())
        for i in range(3):
            embed.add_field(name = data['teams'][i]['teamName'], value = data['teams'][i]['teamName'], inline = True)
        
        embed.set_image(url = data['image']['url'])
        embed.set_footer(text = 'Happy Splatting :)')

        await interaction.response.send_message(embed = embed, view = SplatfestButtons(embed=embed))

async def setup(bot: commands.Bot):
    await bot.add_cog(SplatfestTeamChoices(bot))