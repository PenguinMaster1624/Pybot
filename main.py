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

@bot.event
async def on_ready():
  print(f'{bot.user} at your service')

for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    bot.load_extension('cogs.' + file[:-3])

r = requests.head(url="https://discord.com/api/v1")
try:
  print(f"Rate limit: {int(r.headers['Retry-After']) / 60} minutes left")

except KeyError:
  bot.run(os.getenv('TOKEN'))