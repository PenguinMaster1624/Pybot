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
    def __init__(self) -> None:
        super().__init__(timeout = None)

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
            self.children[num].label = f'{teams}: {len(players[num])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = teams, value = player_list if player_list else None)

        return embed
    
    @discord.ui.button(label = teams[0], style = discord.ButtonStyle.blurple, custom_id = 'Shiver')
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Shiver')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            embed = await self.embed_setup()
            await interaction.response.edit_message(embed = embed, view = self)

    @discord.ui.button(label = teams[1], style = discord.ButtonStyle.red, custom_id = 'Frye')
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Frye')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            embed = await self.embed_setup()
            await interaction.response.edit_message(embed = embed, view = self)

    @discord.ui.button(label = teams[2], style = discord.ButtonStyle.green, custom_id = 'Big_Man')
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Big Man')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            embed = await self.embed_setup()
            await interaction.response.edit_message(embed = embed, view = self) 


class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    async def SplatfestTeams(self, interaction: discord.Interaction):
        data = fetch_data()
        if interaction.user.id != await self.bot.is_owner(interaction.user):
            await interaction.response.send_message(content = 'You need to be the bot owner to use this command', ephemeral = True)
        
        elif data['isVotable'] is not True:
            await interaction.response.send_message('No Splatfest soon', ephemeral = True)
    
        else:
            embed = discord.Embed(title = data['title'], description = f"Start Time: <t:{data}:t>, t:{data['startTime']}:R>\nEnd TIme: <t:{data['endTime']}:t>, t:{data['endTime']}:R>")
            for i in range(3):
                embed.add_field(name = data['teams'][i]['teamName'], value = data['teams'][i]['teamName'], inline = True)
            
            embed.set_image(data['image']['url'])
            embed.set_footer(text = 'Happy Splatting :)')

            await interaction.response.send_message(embed = embed, view = SplatfestButtons())

async def setup(bot: commands.Bot):
    await bot.add_cog(SplatfestTeamChoices(bot))