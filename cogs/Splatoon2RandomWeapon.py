from discord.ext import commands
import random

class Splat2nRandomWeapon(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def rsw(self, ctx, arg = 'General'):
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
             'Brella' : Brella, 'Blaster' : Blaster, 'Brush' : Brush, 'Splatling' : Splatling, 'Hero' : Hero, 'General' : General}
    
    Selection = []

    try:
      random.shuffle(Class[arg])
      Selection.append(random.choice(Class[arg]))
      select = ''.join(Selection)
      await ctx.send('Weapon Line: ' + select + ' - {}'.format(ctx.author.mention))

    except:
      await ctx.send('Please select a class listed in the pinned message. It\'s case sensitive.')

def setup(bot):
  bot.add_cog(Splat2nRandomWeapon(bot))