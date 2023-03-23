from discord.ext import commands
from discord import app_commands
import discord

class ButtonHelp(discord.ui.View):
  def __init__(self, author):
    super().__init__(timeout = 30)
    self.author = author

  async def on_timeout(self):

    for thing in self.children:
      thing.disabled = True

    await self.message.edit(content = 'You took too long without pressing any buttons', embed = None, view = self)

  async def interaction_owner_check(self, interaction: discord.Interaction, embed: discord.Embed):

    if interaction.user == self.author:
      await interaction.response.edit_message(embed = embed, content = None)

    else:
      await interaction.response.send_message(content = 'This is someone else\'s, use the command yourself', ephemeral = True)

  @discord.ui.button(label = 'General Use', style = discord.ButtonStyle.green)
  async def general(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(title = 'General Commands', description = 'A set of available general use commands', color = discord.Color.orange())
    
    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required. All but the first command here are slash commands.')

    embed.add_field(name = 'hello', value = 'Returns a peppy hello. Prefixed by "Pybot." instead of being a slash command', inline = False)
    embed.add_field(name = 'fac', value = 'Flips a coin for you', inline = False)
    embed.add_field(name = 'mt <Message>', value = 'Translates a message into Morse Code and back', inline = False)
    embed.add_field(name = 'bt <Message>', value = 'Translates a message into Binary Code and back', inline = False)
    embed.add_field(name = 'help', value = 'Pulls this up', inline = False)

    await self.interaction_owner_check(interaction = interaction, embed = embed)

  @discord.ui.button(label = 'Mario Kart', style = discord.ButtonStyle.green)
  async def mario_kart(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(title = 'Mario Kart Commands', description = 'A set of available Mario Kart commands', color = discord.Color.orange())
    
    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required. These are all slash commands.')

    embed.add_field(name = 'mk8m', value = 'Returns a map from any cup if no cup is specified. Otherwise, returns one from within that cup', inline = False)
    embed.add_field(name = 'mk8bm', value = 'Like mk8m, but with Battle Mode stages', inline = False)

    await self.interaction_owner_check(interaction = interaction, embed = embed)

  @discord.ui.button(label = 'Splatoon', style = discord.ButtonStyle.green)
  async def splatoon(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(title = 'Splatoon Commands', description = 'A set of available Splatoon 3 commands', color = discord.Color.orange())
    
    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required. These are all slash commands.')
    
    embed.add_field(name = 'rsw [Weapon Class]', value = 'Chooses a random weapon line from Splatoon 3 if no weapon class is specified', inline = False)
    embed.add_field(name = 'rss <Sub Weapon>', value = 'Chooses a random weapon with a specified Sub Weapon in Splatoon 3.', inline = False)
    embed.add_field(name = 'rsp <Special>', value = 'Randomly chooses a weapon with a specified special in Splatoon 3.', inline = False)
    embed.add_field(name = 'pbgm', value = 'Randomly selects a game mode from those available in private battles in Splatoon 3', inline = False)
    embed.add_field(name = 's3_maps', value = 'Displays maps/modes rotations for Turf War, Anarchy Series/Open and Salmon Run in Splatoon 3', inline = False)

    await self.interaction_owner_check(interaction = interaction, embed = embed)

  @discord.ui.button(label = 'Hypixel Skyblock', style = discord.ButtonStyle.green)
  async def hypixel_skyblock(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(title = 'Hypixel Skyblock Commands', description = 'A set of available Hypixel Skyblock commands', color = discord.Color.orange())
    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required. These are all slash commands.')

    embed.add_field(name = 'mayor', value = 'Shows information on Hypixel Skyblock\'s current mayor', inline = False)
    embed.add_field(name = 'election', value = 'Shows information about an ongoing election in Hypixel Skyblock', inline = False)
    embed.add_field(name = 'bz <ItemID>', value = 'Show you price info for a speecified item in Hypixel Skyblock\'s Bazaar', inline = False)

    await self.interaction_owner_check(interaction = interaction, embed = embed)

  @discord.ui.button(label = 'Overwatch 2', style = discord.ButtonStyle.green)
  async def overwatch_two(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(title = 'Overwatch 2 Commands', description = 'A set of available Overwatch commands', color = discord.Color.orange())
    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
    embed.set_footer(text = 'anything in [] are optional, anything in <> are required. These are all slash commands.')

    embed.add_field(name = 'ow_hero', value = 'Rolls a random hero in Overwatch 2, either from all roles or a role you specified', inline = False)

    await self.interaction_owner_check(interaction = interaction, embed = embed)

  @discord.ui.button(label = 'Quit', style = discord.ButtonStyle.red)
  async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
    if interaction.user == self.author:
      for thing in self.children:
        thing.disabled = True

      await interaction.response.edit_message(content = 'Live With Honor, Die With Glory!', embed = None, view = self)
      self.stop()

    else:
      await interaction.response.send_message(content = 'Please use the command yourself', ephemeral = True)

class help(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @app_commands.command(name = 'help', description = 'Pulls up an interactible list of commands separated by type')
  async def help(self, interaction: discord.Interaction):
    await interaction.response.send_message('Which type of commands do you wish to view?', view = ButtonHelp(interaction.user))
    ButtonHelp.message = await interaction.original_response()

async def setup(bot):
  await bot.add_cog(help(bot))