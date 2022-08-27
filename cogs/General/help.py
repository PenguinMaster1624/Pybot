from discord.ext import commands
import discord

class ButtonHelp(discord.ui.View):
  def __init__(self, author) -> None:
    super().__init__(timeout = None)
    self.author = author

  @discord.ui.button(label = 'General Use', style = discord.ButtonStyle.green)
  async def menu(self, interaction = discord.Interaction, button = discord.ui.Button):
    embed = discord.Embed(title = 'General Commands', description = 'A set of available general use commands', color = discord.Color.orange())
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required')

    embed.add_field(name = 'hello', value = 'Returns a peppy hello', inline = False)
    embed.add_field(name = 'choose <option1> <"option 2"> [Option 3] ...', value = 'Chooses an option for you. You can put in as many items as you want', inline = False)
    embed.add_field(name = 'fac', value = 'Flips a coin for you', inline = False)
    embed.add_field(name = 'mt <Message>', value = 'Translates a message into Morse Code and back', inline = False)
    embed.add_field(name = 'bt <Message>', value = 'Translates a message into Binary Code and back', inline = False)
    embed.add_field(name = 'purge <number>', value = "Deletes a specified amount of messages", inline = False)
    embed.add_field(name = 'join', value = 'Joins the voice call you\'re in', inline = False)
    embed.add_field(name = 'dc', value = 'Leaves the voice call it is currently in', inline = False)
    embed.add_field(name = 'help', value = 'Pulls this up', inline = False)
    embed.add_field(name = 'repeat [Channel ID]', value = 'Repeats a message you tell it, and if you specify a channel ID it\'ll say it there', inline = False)

    if interaction.user == self.author:
      await interaction.response.edit_message(embed = embed, content = None)
    else:
      await interaction.response.send_message(content = 'Not your button!', ephemeral = True)

  @discord.ui.button(label = 'Mario Kart', style = discord.ButtonStyle.green)
  async def menu1(self, interaction = discord.Interaction, button = discord.ui.Button):
    embed = discord.Embed(title = 'Mario Kart Commands', description = 'A set of available Mario Kart commands', color = discord.Color.orange())
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required')

    embed.add_field(name = 'mk8m', value = 'Returns a map from any cup if no cup is specified. Otherwise, returns one from within that cup', inline = False)
    embed.add_field(name = 'mk8bm', value = 'Like mk8m, but with Battle Mode stages', inline = False)

    if interaction.user == self.author:
      await interaction.response.edit_message(embed = embed, content = None)
    else:
      await interaction.response.send_message(content = 'Not your button!', ephemeral = True)
  @discord.ui.button(label = 'Splatoon', style = discord.ButtonStyle.green)
  async def menu2(self, interaction = discord.Interaction, button = discord.ui.Button):
    embed = discord.Embed(title = 'Splatoon Commands', description = 'A set of available Splatoon 2 commands', color = discord.Color.orange())
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required')
    
    embed.add_field(name = 'rsw [Weapon Class]', value = 'Chooses a random weapon line from Splatoon 2 if no weapon class is specified', inline = False)
    embed.add_field(name = 'rss <Sub Weapon>', value = 'Chooses a random weapon with a specified Sub Weapon in Splatoon 2', inline = False)
    embed.add_field(name = 'rsp <Special>', value = 'Randomly chooses a weapon with a specified special in Splatoon 2', inline = False)
    embed.add_field(name = 'pbgm', value = 'Randomly selects a game mode from those available in private battles', inline = False)

    if interaction.user == self.author:
      await interaction.response.edit_message(embed = embed, content = None)
    else:
      await interaction.response.send_message(content = 'Not your button!', ephemeral = True)

  @discord.ui.button(label = 'Hypixel Skyblock', style = discord.ButtonStyle.green)
  async def menu3(self, interaction = discord.Interaction, button = discord.ui.Button):
    embed = discord.Embed(title = 'Hypixel Skyblock Commands', description = 'A set of available Hypixel Skyblock commands', color = discord.Color.orange())
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required')

    embed.add_field(name = 'mayor', value = 'Shows information on Hypixel Skyblock\'s current mayor', inline = False)
    embed.add_field(name = 'election', value = 'Shows information about an ongoing election in Hypixel Skyblock', inline = False)
    embed.add_field(name = 'bz <ItemID>', value = 'Show you price info for a speecified item in Hypixel Skyblock\'s Bazaar', inline = False)

    if interaction.user == self.author:
      await interaction.response.edit_message(embed = embed, content = None)
    else:
      await interaction.response.send_message(content = 'Not your button!', ephemeral = True)

  @discord.ui.button(label = 'Quit', style = discord.ButtonStyle.red, row = 2)
  async def quit(self, interaction = discord.Interaction, button = discord.ui.Button):
    
    if interaction.user == self.author:
      for thing in self.children:
        thing.disabled = True
      await interaction.response.edit_message(content = 'May The Wisdom Be With You', embed = None, view = self)

    else:
      await interaction.response.send_message(content = 'Not your button!', ephemeral = True)
    self.stop()

class help(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @commands.command()
  async def help(self, ctx):

    await ctx.reply('Which type of commands do you wish to view?', view = ButtonHelp(ctx.author))

async def setup(bot):
  await bot.add_cog(help(bot))