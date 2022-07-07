from discord.ext import commands

class HelloReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello there, {}'.format(ctx.author.mention))

def setup(bot):
    bot.add_cog(HelloReply(bot))