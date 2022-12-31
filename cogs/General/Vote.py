from discord import app_commands
from discord.ext import commands
import discord

class PollButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.yes = set()
        self.no = set()
        self.total = tuple([self.yes, self.no])
        self.button_labels = ['Onboard', 'Offboard']

    @discord.ui.button(label = 'Onboard: 0', style = discord.ButtonStyle.blurple)
    async def button_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if user_name not in self.no:
            self.yes.add(user_name)
        
        else:
            self.no.remove(user_name)
            self.yes.add(user_name)

        for j in range(len(self.children)):
            self.children[j].label = f'{self.button_labels[j]}: {len(self.total[j])}'

        await interaction.response.edit_message(view = self)
    
    @discord.ui.button(label = 'Offboard: 0', style = discord.ButtonStyle.red)
    async def button_no(self, interaction: discord.Interaction, button:discord.ui.Button):
        user_name = interaction.user.name

        if user_name not in self.yes:
            self.no.add(user_name)

        else:
            self.yes.remove(user_name)
            self.no.add(user_name)

        for j in range(len(self.children)):
            self.children[j].label = f'{self.button_labels[j]}: {len(self.total[j])}'

        await interaction.response.edit_message(view = self)


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.default_permissions(administrator = True)
    @app_commands.command(name = 'poll', description = 'Have people of a server vote for something')
    async def vote(self, interaction: discord.Interaction, want: str):

        embed = discord.Embed(title = 'Vote In Progress!', description = f'{interaction.user.name} wants to know who wants this/these')
        embed.add_field(name = 'The Request', value = f'{interaction.user.name} wants: {want}')
        embed.set_footer(text = 'May the community decide')

        await interaction.response.send_message(embed = embed, view = PollButtons())

async def setup(bot):
    await bot.add_cog(Poll(bot))