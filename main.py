import discord
from discord.ext import commands
import random  
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '.', intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user} at your service')

@bot.command()
async def repeat(ctx, msg, chnl = None):
  await ctx.channel.purge(limit = 1)
  
  if chnl == None:
    await ctx.channel.send(msg)
    
  else:
    place = int(chnl) 
    channel = bot.get_channel(place)
    await channel.send(msg)

@bot.command()
async def hello(ctx):
  await ctx.send('Hello there, {}'.format(ctx.author.mention))

@bot.command()
async def choose(ctx, *choices: str):
  await ctx.send(random.choice(choices))

@bot.command()
async def purge(ctx, amount):
  amount = int(amount)
  await ctx.channel.purge(limit = amount)

for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    bot.load_extension('cogs.' + file[:-3])

bot.run(os.getenv('TOKEN'))