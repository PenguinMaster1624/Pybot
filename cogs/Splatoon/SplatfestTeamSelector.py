from discord import app_commands
from discord.ext import commands
import discord


teams = ['Same Ol\'', 'Bucket List', 'Save the Day', 'Undecided']
class SplatfestButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

        self.total = {
            'Shiver': [],
            'Frye': [],
            'Big Man': [],
            'Undecided': []
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
        for i in range(len(self.children)):
            self.children[i].label = f'{teams[i]}: {len(players[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = teams[j], value = player_list if player_list else None)

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

    @discord.ui.button(label = 'Undecided', style = discord.ButtonStyle.grey, custom_id = 'Undecided')
    async def Undeclared(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(user_name = user_name, team = 'Undecided')

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
        if interaction.user.id != self.bot.is_owner(interaction.user):
            await interaction.response.send_message(content = 'You need to be the bot owner to use this command', ephemeral = True)
    
        else:
            embed = discord.Embed(title = 'Splatfest Teams', description = 'The current Splatfest teams')
            embed.add_field(name = teams[0], value = 'Shiver', inline = True)
            embed.add_field(name = teams[1], value = 'Frye', inline = True)
            embed.add_field(name = teams[2], value = 'Big Man', inline = True)
            embed.add_field(name = teams[3], value = 'Dunno yet')
            embed.set_footer(text = 'If undecided or not participating, choose the gray button')

            await interaction.response.send_message(embed = embed, view = SplatfestButtons())

async def setup(bot: commands.Bot):
    await bot.add_cog(SplatfestTeamChoices(bot))