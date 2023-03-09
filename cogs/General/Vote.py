from discord import app_commands
from discord.ext import commands
import discord

class PollButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.all = {
            'Yay': [],
            'Nay': [],
            'Undecided': []
        }

        self.button_labels = list(self.all.keys())

    @discord.ui.button(label = 'Yay: 0', style = discord.ButtonStyle.blurple)
    async def button_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.all['Nay'], self.all['Undecided']]):
            self.all['Nay'] = [i for i in self.all['Nay'] if i != user_name]
            self.all['Undecided'] = [i for i in self.all['Undecided'] if i != user_name]
            self.all['Yay'].append(user_name)
        
        elif user_name in self.all['Yay']:
            await interaction.response.send_message(content = 'You\'ve already voted in favor!', ephemeral = True)
        
        else:
            self.all['Yay'].append(user_name)
        
        users = list(self.all.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.button_labels[i]}: {len(users[i])}'
            
        await interaction.response.edit_message(view = self)
    
    @discord.ui.button(label = 'Nay: 0', style = discord.ButtonStyle.red)
    async def button_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.all['Yay'], self.all['Undecided']]):
            self.all['Yay'] = [i for i in self.all['Yay'] if i != user_name]
            self.all['Undecided'] = [i for i in self.all['Undecided'] if i != user_name]
            self.all['Nay'].append(user_name)

        elif user_name in self.all['Nay']:
            await interaction.response.send_message(content = 'You\'ve already voted in favor!', ephemeral = True)
        
        else:
            self.all['Nay'].append(user_name)
        
        users = list(self.all.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.button_labels[i]}: {len(users[i])}'
            
        await interaction.response.edit_message(view = self)
    
    @discord.ui.button(label = 'Undecided: 0', style = discord.ButtonStyle.gray)
    async def button_undecided(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_name = interaction.user.name

        if any(user_name in i for i in [self.all['Yay'], self.all['Nay']]):
            self.all['Yay'] = [i for i in self.all['Yay'] if i != user_name]
            self.all['Nay'] = [i for i in self.all['Nay'] if i != user_name]
            self.all['Undecided'].append(user_name)
        
        elif user_name in self.all['Undecided']:
            await interaction.response.send_message(content = 'Your last vote was for this option!', ephemeral = True)
        
        else:
            self.all['Undecided'].append(user_name)

        users = list(self.all.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{self.button_labels[i]}: {len(users[i])}'
        
        await interaction.response.edit_message(view = self)


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.default_permissions(administrator = True)
    @app_commands.command(name = 'poll', description = 'Have people of a server vote for something')
    async def vote(self, interaction: discord.Interaction, want: str):

        embed = discord.Embed(title = 'Vote In Progress!', description = f'{interaction.user.name} has called a vote!')
        embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
        embed.add_field(name = 'The Request', value =  f'{want}')
        embed.set_footer(text = 'May the community decide')

        await interaction.response.send_message(embed = embed, view = PollButtons())

async def setup(bot):
    await bot.add_cog(Poll(bot))