from discord.ext import commands
from discord import app_commands
import discord, random

class RandomChoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = 'choose', description = 'Selects one of the given inputs for you')
    async def choose(self, interaction: discord.Interaction, option_one: str, option_two: str, option_three: str = None, option_four: str = None):
        
        choice = [option_one, option_two]
        if option_three is not None:
            choice.append(option_three)
        
        elif option_four is not None:
            choice.append(option_four)

        choice_select = random.choice(choice)
        await interaction.response.send_message(choice_select)


async def setup(bot):
    await bot.add_cog(RandomChoice(bot))