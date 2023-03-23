from discord.ext import commands, tasks
from discord import app_commands
from zoneinfo import ZoneInfo
import requests
import asyncio
import datetime
import aiohttp
import discord

def time_calc():
    r = requests.get('https://splatoon3.ink/data/schedules.json')
    js = r.json()

    if r.status_code == 200:
      js = js['data']
      turf_war = js['regularSchedules']['nodes'][0]

      end = datetime.datetime.fromisoformat(turf_war['endTime'][:-1])
      end -= datetime.timedelta(hours = 4)

      time = str(datetime.datetime.time(end))
      time = time.split(':')

      new_time = datetime.time(hour = int(time[0]), minute = int(time[1]), second = int(time[2]), tzinfo = ZoneInfo('US/Eastern'))
      return new_time
    

class maps_modes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_send.start()

    async def s3_rotation_update(self):
        images = {}

        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                js = await response.json()

        if response.status == 200:
          js = js['data']
          turf_war = js['regularSchedules']['nodes'][0]

          anarchy_series = js['bankaraSchedules']['nodes'][0]['bankaraMatchSettings'][0]
          anarchy_open = js['bankaraSchedules']['nodes'][0]['bankaraMatchSettings'][1]

          anarchy_series_mode = anarchy_series['vsRule']['name']
          anarchy_open_mode = anarchy_open['vsRule']['name']

          salmon = js['coopGroupingSchedule']['regularSchedules']['nodes'][0]

          start = datetime.datetime.fromisoformat(turf_war['startTime'][:-1])
          start -= datetime.timedelta(hours = 4)
          start = str(start.timestamp())[:-2]
    
          end = datetime.datetime.fromisoformat(turf_war['endTime'][:-1])
          end -= datetime.timedelta(hours = 4)
          end = str(end.timestamp())[:-2]

          salmon_start = datetime.datetime.fromisoformat(salmon['startTime'][:-1])
          salmon_start -= datetime.timedelta(hours = 4)
          salmon_start = str(salmon_start.timestamp())[:-2]
    
          salmon_end = datetime.datetime.fromisoformat(salmon['endTime'][:-1])
          salmon_end -= datetime.timedelta(hours = 4)
          salmon_end = str(salmon_end.timestamp())[:-2]

          for i in range(0, 2):
              turf_maps = turf_war['regularMatchSetting']['vsStages'][i]
              anarchy_series_maps = anarchy_series['vsStages'][i]
              anarchy_open_maps = anarchy_open['vsStages'][i]
              
              images[turf_maps['name']] = turf_maps['image']['url']
              images[anarchy_series_maps['name']] = anarchy_series_maps['image']['url']
              images[anarchy_open_maps['name']] = anarchy_open_maps['image']['url']
        
        images[salmon['setting']['coopStage']['name']] = salmon['setting']['coopStage']['image']['url']

        rotation_update = discord.Embed(title = 'Splatoon 3 Rotations', description = f'Current maps as of <t:{start}:t>, <t:{start}:R>\nUpdates in <t:{end}:R>', color = discord.Color.blue())
        
        turf_one = discord.Embed(color = discord.Color.green())
        turf_one.add_field(name = 'Turf War', value = list(images.keys())[0])
        turf_one.set_image(url = list(images.values())[0])

        turf_two = discord.Embed(description = list(images.keys())[3], color = discord.Color.green())
        turf_two.set_image(url = list(images.values())[3])

        anarchy_series_one = discord.Embed(color = discord.Color.orange())
        anarchy_series_one.add_field(name = f'Anarchy Series - {anarchy_series_mode}', value = list(images.keys())[1])
        anarchy_series_one.set_image(url = list(images.values())[1])

        anarchy_series_two = discord.Embed(description = list(images.keys())[4], color = discord.Color.orange())
        anarchy_series_two.set_image(url = list(images.values())[4])

        anarchy_open_one = discord.Embed(color = discord.Color.dark_orange())
        anarchy_open_one.add_field(name = f'Anarchy Open - {anarchy_open_mode}', value = list(images.keys())[2])
        anarchy_open_one.set_image(url = list(images.values())[2])

        anarchy_open_two = discord.Embed(description = list(images.keys())[5], color = discord.Color.dark_orange())
        anarchy_open_two.set_image(url = list(images.values())[5])

        salmon_run = discord.Embed(title = 'Salmon Run', description = f'Started <t:{salmon_start}:f>, <t:{salmon_start}:R>\nEnds <t:{salmon_end}:f>, <t:{salmon_end}:R>', color = discord.Color.purple())
        salmon_run.add_field(name = list(images.keys())[-1], value = '\n'.join(salmon['setting']['weapons'][i]['name'] for i in range(0, 4)))
        salmon_run.set_image(url = list(images.values())[-1])
        salmon_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')

        return rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run
    
    async def s3_next_rotation(self):
        images = {}

        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                js = await response.json()

        if response.status == 200:
          js = js['data']
          future_turf_war = js['regularSchedules']['nodes'][1]

          future_anarchy_series = js['bankaraSchedules']['nodes'][1]['bankaraMatchSettings'][0]
          future_anarchy_open = js['bankaraSchedules']['nodes'][1]['bankaraMatchSettings'][1]

          future_anarchy_series_mode = future_anarchy_series['vsRule']['name']
          future_anarchy_open_mode = future_anarchy_open['vsRule']['name']

          future_salmon = js['coopGroupingSchedule']['regularSchedules']['nodes'][1]

          start = datetime.datetime.fromisoformat(future_turf_war['startTime'][:-1])
          start -= datetime.timedelta(hours = 4)
          start = str(start.timestamp())[:-2]
    
          end = datetime.datetime.fromisoformat(future_turf_war['endTime'][:-1])
          end -= datetime.timedelta(hours = 4)
          end = str(end.timestamp())[:-2]

          salmon_start = datetime.datetime.fromisoformat(future_salmon['startTime'][:-1])
          salmon_start -= datetime.timedelta(hours = 4)
          salmon_start = str(salmon_start.timestamp())[:-2]
    
          salmon_end = datetime.datetime.fromisoformat(future_salmon['endTime'][:-1])
          salmon_end -= datetime.timedelta(hours = 4)
          salmon_end = str(salmon_end.timestamp())[:-2]

          for i in range(0, 2):
              turf_maps = future_turf_war['regularMatchSetting']['vsStages'][i]
              anarchy_series_maps = future_anarchy_series['vsStages'][i]
              anarchy_open_maps = future_anarchy_open['vsStages'][i]
              
              images[turf_maps['name']] = turf_maps['image']['url']
              images[anarchy_series_maps['name']] = anarchy_series_maps['image']['url']
              images[anarchy_open_maps['name']] = anarchy_open_maps['image']['url']
        
        images[future_salmon['setting']['coopStage']['name']] = future_salmon['setting']['coopStage']['image']['url']

        future_rotation_update = discord.Embed(title = 'Splatoon 3 Rotations', description = f'The next rotation starts at <t:{start}:t>, <t:{start}:R>\nEnds <t:{end}:R>', color = discord.Color.blue())
        
        future_turf_one = discord.Embed(color = discord.Color.green())
        future_turf_one.add_field(name = 'Turf War', value = list(images.keys())[0])
        future_turf_one.set_image(url = list(images.values())[0])

        future_turf_two = discord.Embed(description = list(images.keys())[3], color = discord.Color.green())
        future_turf_two.set_image(url = list(images.values())[3])

        future_anarchy_series_one = discord.Embed(color = discord.Color.orange())
        future_anarchy_series_one.add_field(name = f'Anarchy Series - {future_anarchy_series_mode}', value = list(images.keys())[1])
        future_anarchy_series_one.set_image(url = list(images.values())[1])

        future_anarchy_series_two = discord.Embed(description = list(images.keys())[4], color = discord.Color.orange())
        future_anarchy_series_two.set_image(url = list(images.values())[4])

        future_anarchy_open_one = discord.Embed(color = discord.Color.dark_orange())
        future_anarchy_open_one.add_field(name = f'Anarchy Open - {future_anarchy_open_mode}', value = list(images.keys())[2])
        future_anarchy_open_one.set_image(url = list(images.values())[2])

        future_anarchy_open_two = discord.Embed(description = list(images.keys())[5], color = discord.Color.dark_orange())
        future_anarchy_open_two.set_image(url = list(images.values())[5])

        future_salmon_run = discord.Embed(title = 'Salmon Run', description = f'Starts <t:{salmon_start}:f>, <t:{salmon_start}:R>\nEnds <t:{salmon_end}:f>, <t:{salmon_end}:R>', color = discord.Color.purple())
        future_salmon_run.add_field(name = list(images.keys())[-1], value = '\n'.join(future_salmon['setting']['weapons'][i]['name'] for i in range(0, 4)))
        future_salmon_run.set_image(url = list(images.values())[-1])
        future_salmon_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')

        return future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_salmon_run

    @app_commands.command(name = 's3_maps', description = 'Displays the current rotations for Splatoon 3')
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = 'All'):
        mode = mode.title().strip()
        rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run = await self.s3_rotation_update()

        if mode == 'Turf War':
            await interaction.response.send_message(embeds = [rotation_update, turf_one, turf_two])
        
        elif mode == 'Anarchy Series':
            await interaction.response.send_message(embeds = [rotation_update, anarchy_series_one, anarchy_series_two])
        
        elif mode == 'Anarchy Open':
            await interaction.response.send_message(embeds = [rotation_update, anarchy_open_one, anarchy_open_two])
        
        elif mode == 'Salmon Run':
            await interaction.response.send_message(embed = salmon_run)
        
        elif mode == 'All':
            await interaction.response.send_message(embeds = [rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run])

        else:
            await interaction.response.send_message(content = 'Mode not recognized, please refer to the autofilled section when using the command for available modes', ephemeral = True)
    
    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'Salmon Run']
        return [app_commands.Choice(name = mode, value = mode) for mode in modes if current.lower() in mode.lower()]

    @tasks.loop(time = time_calc())
    async def embed_send(self):
        rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run = await self.s3_rotation_update()
        future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_salmon_run = await self.s3_next_rotation()

        channel = self.bot.get_channel(1088459539147411497)
        await channel.purge()
        await asyncio.sleep(1)

        await channel.send(embeds = [rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run])
        await channel.send(embeds = [future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_salmon_run])
            

    @embed_send.before_loop
    async def before_embed_send_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(maps_modes(bot))