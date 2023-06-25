from discord.ext import commands, tasks
from discord import app_commands
from zoneinfo import ZoneInfo
import requests
import aiohttp
import asyncio
import datetime
import discord

def time_calc() -> datetime.time:
    r = requests.get('https://splatoon3.ink/data/schedules.json')
    js = r.json()

    if r.status_code == 200:
      js = js['data']
      turf_war = js['regularSchedules']['nodes'][0]
      end = datetime.datetime.fromisoformat(turf_war['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC'))
      
      return datetime.time(hour = end.hour, minute = end.minute, second = 30, tzinfo = ZoneInfo('UTC'))

class maps_modes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_send.start()

    async def api_call(self):
        '''
        Makes an API call
        ''' 
        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                js = await response.json()
                return js['data']
                
    async def s3_rotation_update(self, node: int) -> discord.Embed:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                turf_war = await response.json()
                turf_war = turf_war['data']
            
        turf_war = turf_war['regularSchedules']['nodes'][node]

        start = str(datetime.datetime.fromisoformat(turf_war['startTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        end = str(datetime.datetime.fromisoformat(turf_war['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]

        rotation_update = discord.Embed(title = 'Splatoon 3 Rotations', description = f'Start Time: <t:{start}:t>, <t:{start}:R>\nEnd Time: <t:{end}:t>, <t:{end}:R>', color = discord.Color.blue())
        return rotation_update
    
    async def turf_war(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Turf War information
        '''
        turf_stuff = await self.api_call()

        if turf_stuff['currentFest']:
            return None
        
        turf_war_info = turf_stuff['regularSchedules']['nodes'][node]['regularMatchSetting']['vsStages'] 
        turf_stages = {stage['name']: stage['image']['url'] for stage in turf_war_info}

        turf_war_stage_one = discord.Embed(color = discord.Color.green())
        turf_war_stage_one.add_field(name = 'Turf War', value = list(turf_stages.keys())[0])
        turf_war_stage_one.set_image(url = list(turf_stages.values())[0])
        turf_war_stage_one.set_footer(text = 'Turf War Stage One')

        turf_war_stage_two = discord.Embed(description = list(turf_stages.keys())[1], color = discord.Color.green())
        turf_war_stage_two.set_image(url = list(turf_stages.values())[1])
        turf_war_stage_two.set_footer(text = 'Turf War Stage Two')

        return turf_war_stage_one, turf_war_stage_two
    
    async def anarchy_series(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Series information
        '''
        anarchy_stuff = await self.api_call()

        if anarchy_stuff['currentFest']:
            return None
        
        anarchy_series_info = anarchy_stuff['bankaraSchedules']['nodes'][node]['bankaraMatchSettings'][0]
        anarchy_series_stages = {stage['name']: stage['image']['url'] for stage in anarchy_series_info['vsStages']}

        anarchy_series_one = discord.Embed(color = discord.Color.orange())
        anarchy_series_one.add_field(name = f'Anarchy Series - {anarchy_series_info["vsRule"]["name"]}', value = list(anarchy_series_stages.keys())[0])
        anarchy_series_one.set_image(url = list(anarchy_series_stages.values())[0])
        anarchy_series_one.set_footer(text = 'Anarchy Series Stage One')

        anarchy_series_two = discord.Embed(color = discord.Color.orange(), description = list(anarchy_series_stages.keys())[1])
        anarchy_series_two.set_image(url = list(anarchy_series_stages.values())[1])
        anarchy_series_two.set_footer(text = 'Anarchy Series Stage Two')

        return anarchy_series_one, anarchy_series_two
    
    async def anarchy_open(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Open information
        '''
        anarchy_stuff = await self.api_call()

        if anarchy_stuff['currentFest']:
            return None
        
        anarchy_open_info = anarchy_stuff['bankaraSchedules']['nodes'][node]['bankaraMatchSettings'][1]
        anarchy_open_stages = {stage['name']: stage['image']['url'] for stage in anarchy_open_info['vsStages']}

        anarchy_open_one = discord.Embed(color = discord.Color.dark_orange())
        anarchy_open_one.add_field(name = f'Anarchy Open - {anarchy_open_info["vsRule"]["name"]}', value = list(anarchy_open_stages.keys())[0])
        anarchy_open_one.set_image(url = list(anarchy_open_stages.values())[0])
        anarchy_open_one.set_footer(text = 'Anarchy Open Stage One')

        anarchy_open_two = discord.Embed(color = discord.Color.dark_orange(), description = list(anarchy_open_stages.keys())[1])
        anarchy_open_two.set_image(url = list(anarchy_open_stages.values())[1])
        anarchy_open_two.set_footer(text = 'Anarchy Open Stage Two')

        return anarchy_open_one, anarchy_open_two
    
    async def challenges(self, node: int) -> discord.Embed:
        '''
        Returns Challenge information
        '''
        challenge_stuff = await self.api_call()

        challenges_info = challenge_stuff['eventSchedules']['nodes'][node]
        challengs_timeslots = challenges_info['timePeriods']

        challenges_start_one = str(datetime.datetime.fromisoformat(challengs_timeslots[0]['startTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        challenges_start_two = str(datetime.datetime.fromisoformat(challengs_timeslots[1]['startTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        challenges_start_three = str(datetime.datetime.fromisoformat(challengs_timeslots[2]['startTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]

        challenges_end_one = str(datetime.datetime.fromisoformat(challengs_timeslots[0]['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        challenges_end_two = str(datetime.datetime.fromisoformat(challengs_timeslots[1]['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        challenges_end_three = str(datetime.datetime.fromisoformat(challengs_timeslots[2]['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]

        challenges_info = challenges_info['leagueMatchSetting']
        challenges_stages = {stage['name']: stage['image']['url'] for stage in challenges_info['vsStages']}

        regulation = str(challenges_info['leagueMatchEvent']['regulation']).split('<br />')
        regulation = '\n'.join(i.strip('・ ') for i in regulation)

        challenge_one = discord.Embed(title = f'Challenge: {challenges_info["leagueMatchEvent"]["name"]}', 
                                  description = challenges_info['leagueMatchEvent']['desc'],
                                  color = discord.Color.from_rgb(244, 79, 148))
        
        challenge_one.add_field(name = f"{challenges_info['vsRule']['name']} - {list(challenges_stages.keys())[0]} | {list(challenges_stages.keys())[1]}", 
                                value = regulation, 
                                inline = False)
        
        challenge_one.add_field(name = 'Time Slots For This Challenge', 
                                value = f'Starts <t:{challenges_start_one}:F>\nEnds <t:{challenges_end_one}:F>\n\nStarts <t:{challenges_start_two}:F>\nEnds <t:{challenges_end_two}:F>\n\nStarts <t:{challenges_start_three}:F>\nEnds <t:{challenges_end_three}:F>', 
                                inline = False)
        
        challenge_one.set_image(url = list(challenges_stages.values())[0])
        challenge_one.set_footer(text = 'Challenge Stage One')

        challenge_two = discord.Embed(color = discord.Color.from_rgb(244, 79, 148))
        challenge_two.set_image(url = list(challenges_stages.values())[1])
        challenge_two.set_footer(text = 'Challenge Stage Two')

        return challenge_one, challenge_two

    async def salmon_run(self, node: int) -> discord.Embed | None:
        '''
        Returns Salmon Run information in an embed
        '''
        salmon_run_stuff = await self.api_call()

        salmon_run_info = salmon_run_stuff['coopGroupingSchedule']['regularSchedules']['nodes'][node]

        start = str(datetime.datetime.fromisoformat(salmon_run_info['startTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        end = str(datetime.datetime.fromisoformat(salmon_run_info['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]

        maps = salmon_run_info['setting']['coopStage']
        weapons = salmon_run_info['setting']['weapons']
        king_salmonid = salmon_run_info['__splatoon3ink_king_salmonid_guess']

        salmon_run = discord.Embed(title = 'Salmon Run', description = f'Start time: <t:{start}:f>, <t:{start}:R>\nEnd Time: <t:{end}:f>, <t:{end}:R>', color = discord.Color.purple())
        salmon_run.add_field(name = f"{maps['name']} - {king_salmonid}", value = '\n'.join(node['name'] for node in weapons))
        salmon_run.set_image(url = maps['image']['url'])
        salmon_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')
        salmon_run.set_footer(text = 'Powered by **Splatoon3.ink**')

        return salmon_run

    async def big_run(self) -> discord.Embed | None:
        ...
    
    async def eggstra_work(self) -> discord.Embed | None:
        ...
    
    async def splatfest(self, node: int) -> discord.Embed | None:
        ...

            
    @app_commands.command(name = 's3_maps', description = 'Displays the current rotations for Splatoon 3')
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = 'All'):
        mode = mode.title().strip()
        rotation_update = await self.s3_rotation_update(0)
        turf_war_one, turf_war_two = await self.turf_war(0)
        anarchy_series_one, anarchy_series_two = await self.anarchy_series(0)
        anarchy_open_one, anarchy_open_two = await self.anarchy_open(0)
        challenge_one, challenge_two = await self.challenges(0)

        match mode:
            case 'All':
                await interaction.response.send_message(embeds = [rotation_update, turf_war_one, turf_war_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, challenge_one, challenge_two])
            
            case 'Turf War':
                await interaction.response.send_message(embeds = [rotation_update, turf_war_one, turf_war_two])

            case 'Anarchy Series':
                await interaction.response.send_message(embeds = [rotation_update, anarchy_series_one, anarchy_series_two])

            case 'Anarchy Open':
                await interaction.response.send_message(embeds = [rotation_update, anarchy_open_one, anarchy_open_two])
            
            case 'Challenge':
                await interaction.response.send_message(embeds = [challenge_one, challenge_two])
            
            case _:
                await interaction.response.send_message(content = 'That is not a valid game mode', ephemeral = True)

    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'Challenge']
        return [app_commands.Choice(name = mode, value = mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel_id: int):
        
        channel = self.bot.get_channel(channel_id)
        await channel.purge()
        await asyncio.sleep(1)

        rotation_update = await self.s3_rotation_update(0)
        turf_one, turf_two = await self.turf_war(0)
        anarchy_series_one, anarchy_series_two = await self.anarchy_series(0)
        anarchy_open_one, anarchy_open_two = await self.anarchy_open(0)
        challenge_one, challenge_two = await self.challenges(0)
        salmon_run = await self.salmon_run(0)

        future_rotation_update = await self.s3_rotation_update(1)
        future_turf_one, future_turf_two = await self.turf_war(1)
        future_anarchy_series_one, future_anarchy_series_two = await self.anarchy_series(1)
        future_anarchy_open_one, future_anarchy_open_two = await self.anarchy_open(1)
        future_challenge_one, future_challenge_two = await self.challenges(1)
        future_salmon_run = await self.salmon_run(1)

        await channel.send(embeds = [rotation_update, turf_one, turf_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, challenge_one, challenge_two, salmon_run])
        await channel.send(content = '------------------------------------------------')
        await channel.send(embeds = [future_rotation_update, future_turf_one, future_turf_two, future_anarchy_series_one, future_anarchy_series_two, future_anarchy_open_one, future_anarchy_open_two, future_challenge_one, future_challenge_two, future_salmon_run])
    
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