from discord.ext import commands
from discord import app_commands
from datetime import datetime
from zoneinfo import ZoneInfo
import discord
import re


choices = ['I\'m In', 'Not Joining', 'Maybe']
class RallyButtons(discord.ui.View):
    def __init__(self, embed: discord.Embed) -> None:
        super().__init__(timeout = None)

        self.embed = embed
        self.people = {
            choices[0]: [],
            choices[1]: [],
            choices[2]: []
        }
    
    async def player_check(self, player_name: str, choice: str) -> str | None:
        for key, players in self.people.items():
            if key != choice:
                if player_name in players:
                    players.remove(player_name)
            
            elif key == choice and player_name in players:
                return 'You\'ve already made that choice, unless you want to change it to another one'
                
            else:
                players.append(player_name)

    async def embed_setup(self) -> discord.Embed:
        players = list(self.people.values())
        for i in range(len(self.children)):
            self.children[i].label = f'{choices[i]}: {len(players[i])}'

        for j in range(len(players)):
            player_list = '\n'.join(players[j])
            self.embed.set_field_at(index = j, name = choices[j], value = player_list if player_list else None)
            
    
    @discord.ui.button(label = choices[0], style = discord.ButtonStyle.blurple)
    async def button_yeah(self, interaction: discord.Interaction, button: discord.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(player_name = user_name, choice = 'I\'m In')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            await self.embed_setup()
            await interaction.response.edit_message(embed = self.embed, view = self)

    @discord.ui.button(label = choices[1], style = discord.ButtonStyle.danger)
    async def button_no(self, interaction: discord.Interaction, button: discord.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(player_name = user_name, choice = 'Not Joining')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            await self.embed_setup()
            await interaction.response.edit_message(embed = self.embed, view = self)
    
    @discord.ui.button(label = choices[2], style = discord.ButtonStyle.gray)
    async def button_maybe(self, interaction: discord.Interaction, button: discord.Button):
        user_name = interaction.user.display_name
        helper = await self.player_check(player_name = user_name, choice = 'Maybe/Undecided')

        if interaction.response.is_done() == False and helper != None:
            await interaction.response.send_message(content = helper, ephemeral = True)
        
        else:
            await self.embed_setup()
            await interaction.response.edit_message(embed = self.embed, view = self)

class GamersRallyUp(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name = 'rally_players', description = 'See who wants to join you in a game, use m/d for day and h/m for time')
    async def rally_players(self, interaction: discord.Interaction, game: str, day: str = None, time: str = None, role: discord.Role = None) -> None:
        username = interaction.user.display_name
        game = game.title()

        if time is not None:
            formatted_time = list(re.search(r'(\d+:)?(\d+)?([A|a|P|p])', time).groups())

            if formatted_time[0] is None:
                formatted_time[1] = f'{formatted_time[1]}:'
                formatted_time = list(filter(lambda x: x is not None, formatted_time))
                formatted_time.insert(1, '0')

        embed = discord.Embed(title = 'Game Time?',
                              color = discord.Color.orange(),
                              timestamp = datetime.now(tz = ZoneInfo('US/Eastern'))
                              )
        
        embed.set_author(name = username, icon_url = interaction.user.display_avatar)
        embed.add_field(name = 'Joining', value = 'For those who want to join', inline = True)
        embed.add_field(name = 'Not Joining', value = 'For those who don\'t want to join', inline = True)
        embed.add_field(name = 'Maybe', value = 'For those who unsure if they will join', inline = True)
        
        if day is not None and time is not None:
            parsed_date = datetime.strptime(day, '%m/%d').replace(tzinfo = ZoneInfo('US/Eastern'))
            parsed_time = datetime.strptime(f'{formatted_time[0]}{formatted_time[1]}{formatted_time[2]}M'.upper(), '%H:%M%p').replace(tzinfo = ZoneInfo('US/Eastern'))
            parsed_time_info = datetime.combine(parsed_date.date(), 
                                                parsed_time.time(), 
                                                ZoneInfo('US/Eastern')).replace(year = datetime.now(ZoneInfo('US/Eastern')).year)

        elif day is None and time is not None:
            parsed_time_info = datetime.combine(datetime.now().date(), 
                                                datetime.strptime(f'{formatted_time[0]}{formatted_time[1]}{formatted_time[2]}M'.upper(), '%I:%M%p').replace(tzinfo = ZoneInfo('US/Eastern')).time(), 
                                                ZoneInfo('US/Eastern')).replace(year = datetime.now(ZoneInfo('US/Eastern')).year)
        if time is not None and role is not None:
            embed.description = f'{username} wants to play {game} - <t:{int(parsed_time_info.timestamp())}:t> <t:{int(parsed_time_info.timestamp())}:R> {role.mention}'

        elif time is not None and role is None:
            embed.description = f'{username} wants to play {game} - <t:{int(parsed_time_info.timestamp())}:t> <t:{int(parsed_time_info.timestamp())}:R>'

        elif time is None and role is not None:
            embed.description = f'{username} wants to play {game} - {role.mention}'

        else:
            embed.description = f'{username} wants to play {game}'

        await interaction.response.send_message(embed = embed, view = RallyButtons(embed = embed))

async def setup(bot: commands.Bot):
    await bot.add_cog(GamersRallyUp(bot))
        
