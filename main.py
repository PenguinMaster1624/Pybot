from cogs.Splatoon.SplatfestTeamSelector import SplatfestButtons
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level = logging.INFO, handler = handler, root = False)

load_dotenv('./.env')

class Pybot(commands.Bot):
  def __init__(self):
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    
    activity = discord.Game(name = 'The Completion of the 2.0 Migration')
    super().__init__(command_prefix = 'Pybot.', help_command = None, intents = intents, activity = activity)

  async def setup_hook(self) -> None:
    for folder in os.listdir('./cogs'):
      for file in os.listdir('./cogs/' + folder):
        if file.endswith('.py'):
          await self.load_extension(f'cogs.{folder}.{file[:-3]}')

    await self.tree.sync()
    self.add_view(SplatfestButtons())

  async def on_ready(self): 
    print(f'{self.user} at your service')

Bot = Pybot()
Bot.run(token = os.getenv('TOKEN'), log_handler = None)