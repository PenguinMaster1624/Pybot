from cogs.Splatoon.SplatfestTeamSelector import SplatfestButtons
from PackageVersionChecker import package_check
from discord.ext import commands
from dotenv import load_dotenv
import logging
import discord
import os


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level = logging.INFO, handler = handler, root = False)

load_dotenv('./.env')


class Pybot(commands.Bot):
  def __init__(self) -> None:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    activity = discord.Activity(name = "/help", type = discord.ActivityType.listening)
    super().__init__(command_prefix = 'Pybot.', help_command = None, intents = intents, activity = activity)

  async def setup_hook(self) -> None:
    for folder in os.listdir('./cogs'):
      for file in os.listdir('./cogs/' + folder):
        if file.endswith('.py'):
          await self.load_extension(f'cogs.{folder}.{file[:-3]}')

    await self.tree.sync()
    self.add_view(SplatfestButtons())

  async def on_ready(self) -> None:
    await package_check()
    print(f'{self.user} at your service')


if __name__ == '__main__':
  Bot = Pybot()
  Bot.run(token = os.getenv('TOKEN'), log_handler = handler)
  