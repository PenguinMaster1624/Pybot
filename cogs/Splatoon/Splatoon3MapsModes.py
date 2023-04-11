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
      end -= datetime.timedelta(hours = 3, minutes = 59, seconds = 30)

      time = str(datetime.datetime.time(end))
      time = time.split(':')

      new_time = datetime.time(hour = int(time[0]), minute = int(time[1]), second = int(time[2]), tzinfo = ZoneInfo('US/Eastern'))
      return new_time
    

class maps_modes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_send.start()

    async def s3_rotation_update(self, node: int):
        images = {}

        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                js = await response.json()

        if response.status == 200:
            js = js['data']
            turf_war = js['regularSchedules']['nodes'][node]
            
            start = datetime.datetime.fromisoformat(turf_war['startTime'][:-1])
            start -= datetime.timedelta(hours = 4)
            start = str(start.timestamp())[:-2]
            
            end = datetime.datetime.fromisoformat(turf_war['endTime'][:-1])
            end -= datetime.timedelta(hours = 4)
            end = str(end.timestamp())[:-2]
            
            salmon = js['coopGroupingSchedule']['regularSchedules']['nodes'][node]
            salmon_start = datetime.datetime.fromisoformat(salmon['startTime'][:-1])
            salmon_start -= datetime.timedelta(hours = 4)
            salmon_start = str(salmon_start.timestamp())[:-2]
            
            salmon_end = datetime.datetime.fromisoformat(salmon['endTime'][:-1])
            salmon_end -= datetime.timedelta(hours = 4)
            salmon_end = str(salmon_end.timestamp())[:-2]
            
            salmon_boss = salmon['__splatoon3ink_king_salmonid_guess']
            
            images[salmon['setting']['coopStage']['name']] = salmon['setting']['coopStage']['image']['url']
            rotation_update = discord.Embed(title = 'Splatoon 3 Rotations', description = f'Current maps as of <t:{start}:t>, <t:{start}:R>\nUpdates <t:{end}:R>', color = discord.Color.blue())

        if node == 0:
            salmon_run = discord.Embed(title = 'Salmon Run', description = f'Started <t:{salmon_start}:f>, <t:{salmon_start}:R>\nEnds <t:{salmon_end}:f>, <t:{salmon_end}:R>', color = discord.Color.purple())
        
        elif node == 1:
            salmon_run = discord.Embed(title = 'Salmon Run', description = f'Starts <t:{salmon_start}:f>, <t:{salmon_start}:R>\nEnds <t:{salmon_end}:f>, <t:{salmon_end}:R>', color = discord.Color.purple())
            rotation_update.description = f'Next map rotations at <t:{start}:t>, <t:{start}:R>\nUpdates <t:{end}:R>'

        salmon_run.add_field(name = f'{list(images.keys())[0]} - {salmon_boss}', value = '\n'.join(salmon['setting']['weapons'][i]['name'] for i in range(0, 4)))
        salmon_run.set_image(url = list(images.values())[0])
        salmon_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')
        
        if turf_war['festMatchSetting'] == None:
            anarchy_series = js['bankaraSchedules']['nodes'][node]['bankaraMatchSettings'][0]
            anarchy_open = js['bankaraSchedules']['nodes'][node]['bankaraMatchSettings'][1]

            anarchy_series_mode = anarchy_series['vsRule']['name']
            anarchy_open_mode = anarchy_open['vsRule']['name']

            for i in range(0, 2):
                turf_maps = turf_war['regularMatchSetting']['vsStages'][i]
                anarchy_series_maps = anarchy_series['vsStages'][i]
                anarchy_open_maps = anarchy_open['vsStages'][i]

                images[turf_maps['name']] = turf_maps['image']['url']
                images[anarchy_series_maps['name']] = anarchy_series_maps['image']['url']
                images[anarchy_open_maps['name']] = anarchy_open_maps['image']['url']

            turf_one = discord.Embed(color = discord.Color.green())
            turf_one.add_field(name = 'Turf War', value = list(images.keys())[1])
            turf_one.set_image(url = list(images.values())[1])

            turf_two = discord.Embed(description = list(images.keys())[4], color = discord.Color.green())
            turf_two.set_image(url = list(images.values())[4])

            anarchy_series_one = discord.Embed(color = discord.Color.orange())
            anarchy_series_one.add_field(name = f'Anarchy Series - {anarchy_series_mode}', value = list(images.keys())[2])
            anarchy_series_one.set_image(url = list(images.values())[2])

            anarchy_series_two = discord.Embed(description = list(images.keys())[5], color = discord.Color.orange())
            anarchy_series_two.set_image(url = list(images.values())[5])

            anarchy_open_one = discord.Embed(color = discord.Color.dark_orange())
            anarchy_open_one.add_field(name = f'Anarchy Open - {anarchy_open_mode}', value = list(images.keys())[3])
            anarchy_open_one.set_image(url = list(images.values())[3])

            anarchy_open_two = discord.Embed(description = list(images.keys())[6], color = discord.Color.dark_orange())
            anarchy_open_two.set_image(url = list(images.values())[6])

            return rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run
        
        elif turf_war['festMatchSetting']:
              splatfest = js['festSchedules']['nodes'][node]

              for i in range(0, 2):
                  splatfest_maps = splatfest['festMatchSetting']['vsStages'][i]
                  images[splatfest_maps['name']] = splatfest_maps['image']['url']
              
              splatfest_one = discord.Embed(color = discord.Color.green())
              splatfest_one.add_field(name = 'Splatfest Turf War', value = list(images.keys())[1])
              splatfest_one.set_image(url = list(images.values())[1])

              splatfest_two = discord.Embed(color = discord.Color.green(), description = list(images.keys())[2])
              splatfest_two.set_image(url = list(images.values())[2])
              
              return rotation_update, splatfest_one, splatfest_two, salmon_run

    @app_commands.command(name = 's3_maps', description = 'Displays the current rotations for Splatoon 3')
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = 'All'):
        mode = mode.title().strip()
        try:
            rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run = await self.s3_rotation_update(0)
        
        except ValueError:
            rotation_update, splatfest_one, splatfest_two, salmon_run = await self.s3_rotation_update(0)

        if mode == 'Turf War':
            try:
                await interaction.response.send_message(embeds = [rotation_update, turf_one, turf_two])
            
            except UnboundLocalError:
                await interaction.response.send_message(content = 'There is currently no Turf War data, likely due to a Splatfest', ephemeral = True)

        elif mode == 'Anarchy Series':
            try:
                await interaction.response.send_message(embeds = [rotation_update, anarchy_series_one, anarchy_series_two])
            
            except UnboundLocalError:
                await interaction.response.send_message(content = 'There is no Anarchy data, likely due to a Splatfest', ephemeral = True)
        
        elif mode == 'Anarchy Open':
            try:
                await interaction.response.send_message(embeds = [rotation_update, anarchy_open_one, anarchy_open_two])
            
            except UnboundLocalError:
                await interaction.response.send_message(content = 'Currently there is no Anarchy data, probably because of a Splatfest')
        
        elif mode == 'Salmon Run':
            await interaction.response.send_message(embed = salmon_run)
        
        elif mode == 'Splatfest':
            try:
                await interaction.response.send_message(embeds = [rotation_update, splatfest_one, splatfest_two])
            
            except UnboundLocalError:
                await interaction.response.send_message(content = 'There is no Splatfest data currently', ephemeral = True)
        
        elif mode == 'All':
            try:
                await interaction.response.send_message(embeds = [rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run])
            
            except UnboundLocalError:
                await interaction.response.send_message(embeds = [rotation_update, splatfest_one, splatfest_two, salmon_run])

        else:
            await interaction.response.send_message(content = 'Mode not recognized, please refer to the autofilled section when using the command for available modes', ephemeral = True)
    
    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'Salmon Run', 'Splatfest']
        return [app_commands.Choice(name = mode, value = mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel_id: int):
        
        channel = self.bot.get_channel(channel_id)
        await channel.purge()
        await asyncio.sleep(1)

        try:
            rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run = await self.s3_rotation_update(0)
            future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_salmon_run = await self.s3_rotation_update(1)
        
            await channel.send(embeds = [rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, salmon_run])
            await channel.send(content = '------------------------------------------------')
            await channel.send(embeds = [future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_salmon_run])
    
        except ValueError:
            rotation_update, splatfest_one, splatfest_two, salmon_run = await self.s3_rotation_update(0)
            future_rotation, future_splatfest_one, future_splatfest_two, future_salmon_run = await self.s3_rotation_update(1)

            await channel.send(embeds = [rotation_update, splatfest_one, splatfest_two, salmon_run])
            await channel.send(content = '------------------------------------------------')
            await channel.send(embeds = [future_rotation, future_splatfest_one, future_splatfest_two, future_salmon_run])


    @tasks.loop(seconds = 10)
    async def embed_send(self):
        await self.channel_setup(1088459539147411497)
        await self.channel_setup(1089292971033235466)
        
        self.embed_send.change_interval(time = time_calc())

    @embed_send.before_loop
    async def before_embed_send_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(maps_modes(bot))