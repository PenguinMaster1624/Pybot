import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import os

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

activity = discord.Game(name = 'please hold on using me until further notice')
bot = commands.Bot(command_prefix = 'Pybot.', help_command = None, intents = intents, activity = activity)

async def load():
    for folder in os.listdir('./cogs'):
      for file in os.listdir('./cogs/' + folder):
        if file.endswith('.py'):
          await bot.load_extension(f'cogs.{folder}.{file[:-3]}')

@bot.event
async def on_ready():
  print(f'{bot.user} at your service')

@bot.event
async def on_command_error(ctx, exception):
  if isinstance(exception, commands.CommandNotFound):
    await ctx.send('Command not recognized')
  
  else:
    await ctx.send('Something went wrong. Talk to the guy who made me.')
    print(exception)

async def main():
  await load()
  
  try:
    r = requests.head(url="https://discord.com/api/v1")
    TimeLeft = int(r.headers['Retry-After']) / 60

  except KeyError:
    await bot.start(os.getenv('TOKEN'))

  else:
    TotalTime = TimeLeft
    print(f"Rate limited for {TimeLeft/60 if TimeLeft >= 60 else TimeLeft} {'hours' if TotalTime/60 >= 60 else 'minutes'}")

asyncio.run(main())