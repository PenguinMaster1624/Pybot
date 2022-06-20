from discord.ext import commands
import discord
import random

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def rsw(self, ctx, arg = 'General'):

    """A random weapon selector for Splatoon 2"""
    
    Shooter = ['Splattershot Jr.', 'Splattershot', 'Splattershot Pro', 'Aerospray', 'N-ZAP', '.52 Gal', '.96 Gal' 'Jet Squelcher', 'L-3 Nozzlenose', ' H-3 Nozzlenose','Sploosh-O-Matic', 'Splash-O-Matic', 'Squeezer']
    Roller = ['Splat Roller', 'Carbon Roller', 'Flinza Roller', 'Dynamo Roller']
    Charger = ['Splat Charger', 'Squiffer', 'E-Liter', 'Bamboozler', 'Goo Tuber']
    Slosher = ['Slosher', 'Tri Slosher', 'Sloshing Machine', 'Explosher', 'Boblobber']
    Dualies = ['Splat Dualies', 'Dualie Squelchers', 'Tetra Dualies', 'Dapple Dualies', 'Glooga Dualies']
    Brella = ['Splat Brella', 'Tenta Brella', 'Undercover Brella']
    Blaster = ['Blaster', 'Range Blaster', 'Luna Blaster', 'Rapid Blaster', 'Clash Blaster']
    Brush = ['Inkbrush', 'OctoBrush']
    Splatling = ['Heavy Splatling', 'Mini Splatling', 'Hydra Splatling', 'Ballpoint Splatling', 'Nautilus']
    Hero = ['Hero Shot', 'Hero Roller', 'Hero Charger', 'Hero Dualies', 'Hero Brella', 'Hero Splatling', 'Hero Blaster', 'Hero Brush']
    General = list(Shooter + Roller + Charger + Slosher + Dualies + Brella + Blaster + Brush + Splatling)

    Class = {'Shooter' : Shooter, 'Roller' : Roller, 'Charger' : Charger, 'Slosher' : Slosher, 'Dualies' : Dualies,
             'Brella' : Brella, 'Blaster' : Blaster, 'Brush' : Brush, 'Splatling' : Splatling, 'Hero' : Hero, 'General' : General,
            'shooter' : Shooter, 'roller' : Roller, 'charger' : Charger, 'slosher' : Slosher, 'dualies' : Dualies,
             'brella' : Brella, 'blaster' : Blaster, 'brush' : Brush, 'splatling' : Splatling, 'hero' : Hero, 'general' : General}

    try:
      Selection = []
      random.shuffle(Class[arg])
      Selection.append(random.choice(Class[arg]))
      select = ''.join(Selection)

      embed = discord.Embed(title = 'Splatoon 2 Random Weapon Line Selector', description = 'Scopes go with their respective charger lines', color = discord.Color.random())
      embed.add_field(name = 'Weapon Line:', value = select)
      embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
      embed.set_footer(text = 'You can choose any weapon within the line')
      await ctx.send(embed = embed)

    except KeyError:
      await ctx.send('Something went wrong. Maybe you misspelled something?')

def setup(bot):
  bot.add_cog(Splat2nRandomWeapon(bot))