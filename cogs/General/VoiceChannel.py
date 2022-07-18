from discord.ext import commands

class VC(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def join(self, ctx):
    
    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
      return await ctx.voice_client.move_to(channel)
        
    await channel.connect()
    await ctx.channel.send('Connected!')

  @commands.command()
  async def dc(self, ctx):
    await ctx.voice_client.disconnect()
    await ctx.channel.send('Disconnected!')

def setup(bot):
  bot.add_cog(VC(bot))