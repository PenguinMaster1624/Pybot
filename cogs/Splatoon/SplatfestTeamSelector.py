from discord import app_commands
from discord.ext import commands
import discord

class SplatfestButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.total = {
            'Shiver': [],
            'Frye': [],
            'Big Man': [],
            'Undecided': []
        }
        self.teams = ['Team A', 'Team B', 'Team C', 'Undecided']
    
    @discord.ui.button(label = 'Team A', style = discord.ButtonStyle.blurple, custom_id = 'Shiver')
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.total['Frye'], self.total['Big Man'], self.total['Undecided']]):
            self.total['Frye'] = [i for i in self.total['Frye'] if i != user_name]
            self.total['Big Man'] = [i for i in self.total['Big Man'] if i != user_name]
            self.total['Undecided'] = [i for i in self.total['Undecided'] if i != user_name]
            self.total['Shiver'].append(user_name)
        
        elif user_name in self.total['Shiver']:
            await interaction.response.send_message(content = 'You cannot vote for the team you\'re already on!', ephemeral = True)

        else:
            self.total['Shiver'].append(user_name)

        players = list(self.total.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.teams[i]}: {len(players[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = self.teams[j], value = player_list if player_list else None)
    
        await interaction.response.edit_message(embed = embed, view = self)

    @discord.ui.button(label = 'Team B', style = discord.ButtonStyle.red, custom_id = 'Frye')
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.total['Shiver'], self.total['Big Man'], self.total['Undecided']]):
            self.total['Shiver'] = [i for i in self.total['Shiver'] if i != user_name]
            self.total['Big Man'] = [i for i in self.total['Big Man'] if i != user_name]
            self.total['Undecided'] = [i for i in self.total['Undecided'] if i != user_name]
            self.total['Frye'].append(user_name)
        
        elif user_name in self.total['Frye']:
            await interaction.response.send_message(content = 'You cannot vote for the team you\'re already on!', ephemeral = True)

        else:
            self.total['Frye'].append(user_name)

        players = list(self.total.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.teams[i]}: {len(players[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = self.teams[j], value = player_list if player_list else None)
    
        await interaction.response.edit_message(embed = embed, view = self)

    @discord.ui.button(label = 'Team C', style = discord.ButtonStyle.green, custom_id = 'Big_Man')
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.total['Shiver'], self.total['Frye'], self.total['Undecided']]):
            self.total['Shiver'] = [i for i in self.total['Shiver'] if i != user_name]
            self.total['Frye'] = [i for i in self.total['Frye'] if i != user_name]
            self.total['Undecided'] = [i for i in self.total['Undecided'] if i != user_name]
            self.total['Big Man'].append(user_name)
        
        elif user_name in self.total['Big Man']:
            await interaction.response.send_message(content = 'You cannot vote for the team you\'re already on!', ephemeral = True)

        else:
            self.total['Big Man'].append(user_name)

        players = list(self.total.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.teams[i]}: {len(players[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = self.teams[j], value = player_list if player_list else None)
    
        await interaction.response.edit_message(embed = embed, view = self)        

    @discord.ui.button(label = 'Undecided', style = discord.ButtonStyle.grey, custom_id = 'Undecided')
    async def Undeclared(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.total['Shiver'], self.total['Frye'], self.total['Big Man']]):
            self.total['Shiver'] = [i for i in self.total['Shiver'] if i != user_name]
            self.total['Frye'] = [i for i in self.total['Frye'] if i != user_name]
            self.total['Big Man'] = [i for i in self.total['Big Man'] if i != user_name]
            self.total['Undecided'].append(user_name)
        
        elif user_name in self.total['Undecided']:
            await interaction.response.send_message(content = 'You cannot vote for the team you\'re already on!', ephemeral = True)

        else:
            self.total['Undecided'].append(user_name)

        players = list(self.total.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.teams[i]}: {len(players[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            embed.add_field(name = self.teams[j], value = player_list if player_list else None)
    
        await interaction.response.edit_message(embed = embed, view = self)


class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    async def SplatfestTeams(self, interaction: discord.Interaction):

        embed = discord.Embed(title = 'Splatfest Teams', description = 'The current Splatfest teams')
        embed.add_field(name = 'Team A', value = 'Shiver', inline = True)
        embed.add_field(name = 'Team B', value = 'Frye', inline = True)
        embed.add_field(name = 'Team C', value = 'Big Man', inline = True)
        embed.add_field(name = 'Undecided', value = 'Dunno yet')
        embed.set_footer(text = 'If undecided or not participating, choose the gray button')
        
        await interaction.response.send_message(embed = embed, view = SplatfestButtons())

async def setup(bot):
    await bot.add_cog(SplatfestTeamChoices(bot))