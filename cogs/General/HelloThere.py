from discord.ext import commands

class HelloReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello there, {ctx.author.mention}')

async def setup(bot: commands.Bot):
    await bot.add_cog(HelloReply(bot))