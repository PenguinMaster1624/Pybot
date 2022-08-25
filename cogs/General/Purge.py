from discord.ext import commands
from discord.ext.commands import MissingPermissions

class purge(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.has_permissions(manage_messages = True)
  @commands.command()
  async def purge(self, ctx, amount: int):
    await ctx.channel.purge(limit = amount + 1)

  @purge.error
  async def PurgeError(self, ctx, error):
    if isinstance(error, MissingPermissions):
      await ctx.send('You don\'t have permission to use this command')

async def setup(bot):
  await bot.add_cog(purge(bot))