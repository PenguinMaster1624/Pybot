from discord.ext import commands
import random

class RandomChoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *choices: str):
        choice = random.choice(choices)
        await ctx.send(choice)

def setup(bot):
    bot.add_cog(RandomChoice(bot))