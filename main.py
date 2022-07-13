import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import os

load_dotenv()
intents = discord.Intents.default()
intents.members = True

activity = discord.Game(name = 'under the hood')
bot = commands.Bot(command_prefix = 'Pybot.', help_command = None, intents = intents, activity = activity)

for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    bot.load_extension('cogs.' + file[:-3])

@bot.event
async def on_ready():
  print(f'{bot.user} at your service')

@bot.event
async def on_command_error(ctx, exception):
  if isinstance(exception, commands.CommandNotFound):
    await ctx.send('Command not recognized')

try:
  r = requests.head(url="https://discord.com/api/v1")
  TimeLeft = int(r.headers['Retry-After']) / 60

except KeyError:
  bot.run(os.getenv('TOKEN'))

else:
  TotalTime = TimeLeft
  print(f"Rate limited for {TimeLeft/60 if TimeLeft >= 60 else TimeLeft} {'hours' if TotalTime/60 >= 60 else 'minutes'}")