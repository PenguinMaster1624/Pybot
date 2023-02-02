from discord import app_commands
from discord.ext import commands
import discord

class SplatfestButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.shiver = set()
        self.frye = set()
        self.big_man = set()
        self.undecided = set()
        self.total = [self.shiver, self.frye, self.big_man, self.undecided]
        self.teams = ['Team A', 'Team B', 'Team C', 'Undecided']
    
    @discord.ui.button(label = 'Team A', style = discord.ButtonStyle.blurple, custom_id = 'Shiver')
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name
        
        for i in range(len(self.total)):
            if user_name in self.total[i]:
                self.total[i].discard(user_name)

        self.shiver.add(user_name)

        for i in range(len(self.children)):  
            self.children[i].label = f'{self.teams[i]}: {len(self.total[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(self.total)):
            embed.add_field(name = self.teams[j], value = self.total[j])

        await interaction.response.edit_message(embed = embed, view = self)

    @discord.ui.button(label = 'Team B', style = discord.ButtonStyle.red, custom_id = 'Frye')
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name
        
        for i in range(len(self.total)):
            if user_name in self.total[i]:
                self.total[i].discard(user_name)

        self.frye.add(interaction.user.name)

        for i in range(len(self.children)):  
            self.children[i].label = f'{self.teams[i]}: {len(self.total[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(self.total)):
            embed.add_field(name = self.teams[j], value = self.total[j])

        await interaction.response.edit_message(embed = embed, view = self)
        

    @discord.ui.button(label = 'Team C', style = discord.ButtonStyle.green, custom_id = 'Big_Man')
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name
        
        for i in range(len(self.total)):
            if user_name in self.total[i]:
                self.total[i].discard(user_name)

        self.big_man.add(user_name)

        for i in range(len(self.children)):
            self.children[i].label = f'{self.teams[i]}: {len(self.total[i])}'

        embed = discord.Embed(title = 'Splatfest Teams', colour =  discord.Color.orange())
        for j in range(len(self.total)):
            embed.add_field(name = self.teams[j], value = self.total[j])

        await interaction.response.edit_message(embed = embed, view = self)
        

    @discord.ui.button(label = 'Undecided', style = discord.ButtonStyle.grey, custom_id = 'Undecided')
    async def Undeclared(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    async def SplatfestTeams(self, interaction: discord.Interaction):

        embed = discord.Embed(title = 'Splatfest Teams', description = 'The current Splatfest teams')
        embed.add_field(name = 'Team A', value = 'Shiver')
        embed.add_field(name = 'Team B', value = 'Frye')
        embed.add_field(name = 'Team C', value = 'Big Man')
        embed.set_footer(text = 'If undecided or not participating, choose the gray button')
        
        await interaction.response.send_message(embed = embed, view = SplatfestButtons())

async def setup(bot):
    await bot.add_cog(SplatfestTeamChoices(bot))