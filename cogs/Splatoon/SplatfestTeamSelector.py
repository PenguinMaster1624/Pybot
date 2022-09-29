from discord import app_commands
from discord.ext import commands
import discord

class SplatfestButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.shiver = []
        self.frye = []
        self.big_man = []
        self.undecided = []
        self.total = [self.shiver, self.frye, self.big_man, self.undecided]
        self.names = ['Team Gear: ', 'Team Grub: ', 'Team Fun: ', 'Undecided: ']
    
    @discord.ui.button(label = 'Team Gear', style = discord.ButtonStyle.blurple, custom_id = 'Shiver')
    async def Shiver(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_info = {interaction.user.id: interaction.user.name}

        for i in range(len(self.total)):
            if user_info in self.total[i]:
                self.total[i].remove(user_info)

        if user_info not in self.shiver:
            self.shiver.append(user_info)
            for j in range(len(self.children)):
                self.children[j].label = f'{self.names[j]}{len(self.total[j])}'

        await interaction.response.edit_message(view = self)

    @discord.ui.button(label = 'Team Grub', style = discord.ButtonStyle.red, custom_id = 'Frye')
    async def Frye(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_info = {interaction.user.id: interaction.user.name}

        for i in range(len(self.total)):
            if user_info in self.total[i]:
                self.total[i].remove(user_info)

        if user_info not in self.frye:
            self.frye.append(user_info)
            for j in range(len(self.children)):
                self.children[j].label = f'{self.names[j]}{len(self.total[j])}'

        await interaction.response.edit_message(view = self)

    @discord.ui.button(label = 'Team Fun', style = discord.ButtonStyle.green, custom_id = 'Big_Man')
    async def Beeg_Man(self, interaction: discord.Interaction, button: discord.ui.Button):
      
        user_info = {interaction.user.id: interaction.user.name}

        for i in range(len(self.total)):
            if user_info in self.total[i]:
                self.total[i].remove(user_info)


        if user_info not in self.big_man:
            self.big_man.append(user_info)
            for j in range(len(self.children)):
                self.children[j].label = f'{self.names[j]}{len(self.total[j])}'

        await interaction.response.edit_message(view = self)

    @discord.ui.button(label = 'Undecided', style = discord.ButtonStyle.grey, custom_id = 'Undecided')
    async def Undeclared(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_info = {interaction.user.id: interaction.user.name}

        for i in range(len(self.total)):
            if user_info in self.total[i]:
                self.total[i].remove(user_info)

        if user_info not in self.undecided:
            self.undecided.append(user_info)
            for j in range(len(self.children)):
                self.children[j].label = f'{self.names[j]}{len(self.total[j])}'

        await interaction.response.edit_message(view = self)
        

class SplatfestTeamChoices(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = 'splatfest', description = 'Sends an embed in which people vote for which Splatfest Team they\'re on')
    async def SplatfestTeams(self, interaction: discord.Interaction):
        if interaction.user.id != 347553488697294848:
            await interaction.response.send_message('You aren\'t the guy who made me!', ephemeral = True)
            return

        embed = discord.Embed(title = 'Splatfest Teams', description = 'The current Splatfest teams')
        embed.add_field(name = 'Team Gear', value = 'Shiver')
        embed.add_field(name = 'Team Grub', value = 'Frye')
        embed.add_field(name = 'Team Fun', value = 'Big Man')
        embed.set_footer(text = 'If undecided or not participating, choose the gray button')
        
        await interaction.response.send_message(embed = embed, view = SplatfestButtons())

async def setup(bot):
    await bot.add_cog(SplatfestTeamChoices(bot))