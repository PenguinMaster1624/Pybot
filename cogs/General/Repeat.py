from discord.ext import commands

class Repeat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def repeat(self, ctx, msg, channel = None):
        await ctx.channel.purge(limit = 1)
    
        if channel == None:
            await ctx.send(msg)

        elif channel != None:
            chnl = self.bot.get_channel(int(channel))
            await chnl.send(msg)

async def setup(bot):
    await bot.add_cog(Repeat(bot))