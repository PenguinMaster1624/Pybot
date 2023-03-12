from discord.ext import commands
from discord import app_commands
import discord, requests, os

# This will all be built upon on a later date, with a greater understanding of the Twitter API
class TwitterStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bearer = os.getenv("TWITTER_BEARER_TOKEN")

async def setup(bot: commands.Bot):
    await bot.add_cog(TwitterStuff(bot))