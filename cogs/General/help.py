from discord.ext import commands
import discord

class help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    embed = discord.Embed(title = 'Usable Commands', description = 'A set of available commands', color = discord.Color.orange())
    embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

    embed.add_field(name = 'hello', value = 'Returns a peppy hello', inline = False)
    embed.add_field(name = 'choose <option1> <"option 2"> [Option 3] ...', value = 'Chooses an option for you. You can put in as many items as you want', inline = True)
    embed.add_field(name = 'fac', value = 'Flips a coin for you', inline = True)
    embed.add_field(name = 'mt <Message>', value = 'Translates a message into Morse Code and back')
    embed.add_field(name = 'bt <Message>', value = 'Translates a message into Binary Code and back')
    embed.add_field(name = 'purge <number>', value = "Deletes a specified amount of messages", inline = False)
    embed.add_field(name = 'join', value = 'Joins the voice call you\'re in', inline = True)
    embed.add_field(name = 'dc', value = 'Leaves the voice call it is currently in', inline = True)
    embed.add_field(name = 'help', value = 'Pulls this up', inline = True)
    embed.add_field(name = 'repeat [Channel ID]', value = 'Repeats a message you tell it, and if you specify a channel ID it\'ll say it there' )

    embed.add_field(name = 'mk8m', value = 'Returns a map from any cup if no cup is specified. Otherwise, returns one from within that cup', inline = False)
    embed.add_field(name = 'mk8bm', value = 'Like mk8m, but with Battle Mode stages', inline = False)
    
    embed.add_field(name = 'rsw [Weapon Class]', value = 'Chooses a random weapon line from Splatoon 2 if no weapon class is specified', inline = False)
    embed.add_field(name = 'rss <Sub Weapon>', value = 'Chooses a random weapon with a specified Sub Weapon in Splatoon 2')
    embed.add_field(name = 'rsp <Special>', value = 'Randomly chooses a weapon with a specified special in Splatoon 2')
    embed.add_field(name = 'pbgm', value = 'Randomly selects a game mode from those available in private battles')
    
    embed.add_field(name = 'mayor', value = 'Shows information on Hypixel Skyblock\'s current mayor', inline = False)
    embed.add_field(name = 'election', value = 'Shows information about an ongoing election in Hypixel Skyblock', inline = True)
    embed.add_field(name = 'bz <ItemID>', value = 'Show you price info for a speecified item in Hypixel Skyblock\'s Bazaar', inline = True)
    embed.add_field(name = 'ah <Item Name>', value = 'Shows you price info on a specified item imn Hypixel Skyblock\'s Auction House', inline = True)

    await ctx.send(embed = embed)
def setup(bot):
  bot.add_cog(help(bot))