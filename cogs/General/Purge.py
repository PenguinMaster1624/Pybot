import discord
from discord import app_commands
from discord.ext import commands

class message_clear(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = 'purge', description = 'deletes a specified amount of messages')
    async def purge(self, interaction: discord.Interaction, num_of_messages: int):
        await interaction.response.defer(ephemeral = True)
        
        await interaction.original_response()
        await interaction.channel.purge(limit = num_of_messages, before = await interaction.original_response())
        
        await interaction.followup.send(f'Deleted {num_of_messages} messages!')

async def setup(bot):
  await bot.add_cog(message_clear(bot))