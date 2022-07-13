from discord.ext import commands
import random

class RandomChoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *choices: str):
        choice = random.choice(choices)
        await ctx.send(choice)

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send('You forgot to close something with another double quote')
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('I need something to work with, I can\'t read your mind and choose from there')

def setup(bot):
    bot.add_cog(RandomChoice(bot))