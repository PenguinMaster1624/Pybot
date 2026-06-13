from PackageVersionChecker import package_check
from utils.logger_config import LOGGING_CONFIG
from utils.errors import OutdatedPackagesError
from utils.sessions import get_session
from discord.ext import commands
from dotenv import load_dotenv
from logging import config
from logging import handlers
import logging
import discord
import os

load_dotenv('.env')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Pybot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        activity = discord.Activity(name="/help", type=discord.ActivityType.listening)
        super().__init__(command_prefix='Pybot.', help_command=None, intents=intents, activity=activity)

    async def setup_hook(self) -> None:
        for folder in os.listdir('./cogs'):
            for file in os.listdir('./cogs/' + folder):
                if file.endswith('.py'):
                    await self.load_extension(f'cogs.{folder}.{file[:-3]}')

        await self.tree.sync()
        await get_session()

    async def on_ready(self) -> None:
        try:
            await package_check()
            logger.info('Pybot, at your command!')

        except OutdatedPackagesError as error:
            logger.warning(error)

if __name__ == '__main__':
    Bot = Pybot()
    Bot.run(token=os.getenv('TOKEN'), log_handler=None)
