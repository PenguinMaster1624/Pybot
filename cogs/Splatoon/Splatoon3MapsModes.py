from discord.ext import commands, tasks
from discord import app_commands
from zoneinfo import ZoneInfo
from GameModeClasses import *
import requests
import aiohttp
import asyncio
import datetime
import discord


def time_calc() -> datetime.time:
    response = requests.get('https://splatoon3.ink/data/schedules.json')

    if response.status_code == 200:
      js = response.json()
      js = js['data']

      turf_war = js['regularSchedules']['nodes'][0]
      end = datetime.datetime.fromisoformat(turf_war['endTime'][:-1]).replace(tzinfo = ZoneInfo('UTC'))
      
      return datetime.time(hour = end.hour, minute = end.minute, second = 30, tzinfo = ZoneInfo('UTC'))

class maps_modes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.embed_send.start()
        self.schedules = None

    async def api_call(self) -> None:
        '''
        Makes an API call
        ''' 
        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                js: dict = await response.json()

            js = js['data']
            modes = ApiResponse(TurfWar = js['regularSchedules']['nodes'], 
                                Anarchy = js['bankaraSchedules']['nodes'], 
                                SalmonRun = js['coopGroupingSchedule']['regularSchedules']['nodes'],
                                Challenge = js['eventSchedules']['nodes'], 
                                XBattles = js['xSchedules']['nodes'],
                                BigRun = js['coopGroupingSchedule']['bigRunSchedules'],
                                EggstraWork = js['coopGroupingSchedule']['teamContestSchedules']
            )
            self.schedules = modes
            
    async def generate_timestamp(self, time: str) -> str:
        '''
        Generates a timestamp as a string for use in Discord Embeds
        '''
        new_time = str(datetime.datetime.fromisoformat(time[:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        return new_time
                
    async def s3_rotation_update(self, node: int) -> discord.Embed:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://splatoon3.ink/data/schedules.json') as response:
                turf_war = await response.json()
                turf_war = turf_war['data']
            
        turf_war = turf_war['regularSchedules']['nodes'][node]
        start = await self.generate_timestamp(turf_war['startTime'])
        end = await self.generate_timestamp(turf_war['endTime'])

        rotation_update = discord.Embed(title = 'Splatoon 3 Rotations', description = f'Start Time: <t:{start}:t>, <t:{start}:R>\nEnd Time: <t:{end}:t>, <t:{end}:R>', color = discord.Color.blue())
        return rotation_update
    
    async def turf_war(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Turf War information
        '''
        modes = self.schedules

        try:
            turf_war = modes.TurfWar[node]
            stage_one = Stage(name = turf_war['regularMatchSetting']['vsStages'][0]['name'], 
                              image = turf_war['regularMatchSetting']['vsStages'][0]['image']['url'])
            
            stage_two = Stage(name = turf_war['regularMatchSetting']['vsStages'][1]['name'], 
                              image = turf_war['regularMatchSetting']['vsStages'][1]['image']['url'])
            
        except IndexError:
            return None, None
        
        turf_info = TurfWar(times = TimeSlots(start = await self.generate_timestamp(turf_war['startTime']), end = await self.generate_timestamp(turf_war['endTime'])),
                            maps = [stage_one, stage_two])

        turf_war_stage_one = discord.Embed(color = discord.Color.green())
        turf_war_stage_one.add_field(name = 'Turf War', value = '')
        turf_war_stage_one.set_image(url = turf_info.maps[0].image)
        turf_war_stage_one.set_footer(text = turf_info.maps[0].name)

        turf_war_stage_two = discord.Embed(color = discord.Color.green())
        turf_war_stage_two.set_image(url = turf_info.maps[1].image)
        turf_war_stage_two.set_footer(text = turf_info.maps[1].name)

        return turf_war_stage_one, turf_war_stage_two
    
    async def anarchy_series(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Series information
        '''
        nodes = self.schedules

        try:
            anarchy_series = nodes.Anarchy[node]['bankaraMatchSettings'][0]
            stage_one = Stage(name = anarchy_series['vsStages'][0]['name'], 
                              image = anarchy_series['vsStages'][0]['image']['url'])
            
            stage_two = Stage(name = anarchy_series['vsStages'][1]['name'],
                              image = anarchy_series['vsStages'][1]['image']['url'])
        
        except IndexError:
            return None, None
        
        series_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(nodes.Anarchy[node]['startTime']), 
                                                      end = await self.generate_timestamp(nodes.Anarchy[node]['endTime'])), 
                                    maps = [stage_one, stage_two],
                                    gamemode = anarchy_series['vsRule']['name'])

        anarchy_series_one = discord.Embed(color = discord.Color.orange())
        anarchy_series_one.add_field(name = f'Anarchy Series - {series_info.gamemode}', value = '')
        anarchy_series_one.set_image(url = series_info.maps[0].image)
        anarchy_series_one.set_footer(text = series_info.maps[0].name)

        anarchy_series_two = discord.Embed(color = discord.Color.orange())
        anarchy_series_two.set_image(url = series_info.maps[1].image)
        anarchy_series_two.set_footer(text = series_info.maps[1].name)

        return anarchy_series_one, anarchy_series_two
    
    async def anarchy_open(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Open information
        '''
        nodes = self.schedules
        
        try:
            anarchy_open = nodes.Anarchy[node]['bankaraMatchSettings'][1]

            stage_one = Stage(name = anarchy_open['vsStages'][0]['name'], 
                              image = anarchy_open['vsStages'][0]['image']['url'])
            
            stage_two = Stage(name = anarchy_open['vsStages'][1]['name'],
                              image = anarchy_open['vsStages'][1]['image']['url'])

        except IndexError:
            return None, None
        
        open_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(nodes.Anarchy[node]['startTime']), 
                                                      end = await self.generate_timestamp(nodes.Anarchy[node]['endTime'])), 
                                    maps = [stage_one, stage_two],
                                    gamemode = anarchy_open['vsRule']['name'])

        anarchy_open_one = discord.Embed(color = discord.Color.dark_orange())
        anarchy_open_one.add_field(name = f'Anarchy Open - {open_info.gamemode}', value = '')
        anarchy_open_one.set_image(url = open_info.maps[0].image)
        anarchy_open_one.set_footer(text = open_info.maps[0].name)

        anarchy_open_two = discord.Embed(color = discord.Color.dark_orange())
        anarchy_open_two.set_image(url = open_info.maps[1].image)
        anarchy_open_two.set_footer(text = open_info.maps[1].name)

        return anarchy_open_one, anarchy_open_two
    
    async def x_battles(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 X Battle information
        '''

        nodes = self.schedules

        try:
            x_battles = nodes.XBattles[node]['xMatchSetting']

            stage_one = Stage(name = x_battles['vsStages'][0]['name'], 
                              image = x_battles['vsStages'][0]['image']['url'])
            
            stage_two = Stage(name = x_battles['vsStages'][1]['name'],
                              image = x_battles['vsStages'][1]['image']['url'])
        
        except IndexError:
            return None, None
        
        x_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(nodes.Anarchy[node]['startTime']), 
                                          end = await self.generate_timestamp(nodes.Anarchy[node]['endTime'])), 
                        maps = [stage_one, stage_two],
                        gamemode = x_battles['vsRule']['name'])

        x_one = discord.Embed(color = discord.Color.dark_green())
        x_one.add_field(name = f'X Battle - {x_info.gamemode}', value = '')
        x_one.set_image(url = x_info.maps[0].image)
        x_one.set_footer(text = x_info.maps[0].name)

        x_two = discord.Embed(color = discord.Color.dark_green())
        x_two.set_image(url = x_info.maps[1].image)
        x_two.set_footer(text = x_info.maps[1].name)

        return x_one, x_two
    
    async def challenges(self, node: int) -> discord.Embed | None:
        '''
        Returns Challenge information
        '''

        challenge_stuff = self.schedules.Challenge

        try:
            challenges_info = challenge_stuff[node]
            challenges_timeslots = challenges_info['timePeriods']
            challenges_info = challenges_info['leagueMatchSetting']
            challenge_maps = challenges_info['vsStages']


        except IndexError:
            return None, None
        
        regulation = str(challenges_info['leagueMatchEvent']['regulation']).split('<br />')
        regulation = '\n'.join(i.strip('・ ') for i in regulation)

        desc = str(challenges_info['leagueMatchEvent']['desc']).split('<br />')
        desc = '\n'.join(i.strip('・ ') for i in desc)

        challenges = Challenge(title = challenges_info['leagueMatchEvent']['name'],
                               description = desc,
                               extended_description = regulation,
                               times = [TimeSlots(start = await self.generate_timestamp(challenges_timeslots[slot]['startTime']),
                                                  end = await self.generate_timestamp(challenges_timeslots[slot]['endTime'])) for slot, data in enumerate(challenges_timeslots)],
                                maps = [Stage(name = challenge_maps[i]['name'], image = challenge_maps[i]['image']['url']) for i in range(2)],
                                gamemode = challenges_info['vsRule']['name'])

        challenge_one = discord.Embed(title = f'Challenge: {challenges.title}', 
                                  description = challenges.description,
                                  color = discord.Color.from_rgb(244, 79, 148))
        
        challenge_one.add_field(name = f"{challenges.gamemode} - {challenges.maps[0].name} | {challenges.maps[1].name}", 
                                value = challenges.extended_description,
                                inline = False)
        
        challenge_one.add_field(name = 'Time Slots For This Challenge', 
                                value = f'''
                                Starts <t:{challenges.times[0].start}:F> <t:{challenges.times[0].start}:R>\nEnds <t:{challenges.times[0].end}:F> <t:{challenges.times[0].end}:R>\n
                                Starts <t:{challenges.times[1].start}:F> <t:{challenges.times[1].start}:R>\nEnds <t:{challenges.times[1].end}:F> <t:{challenges.times[1].end}:R>\n
                                Starts <t:{challenges.times[2].start}:F> <t:{challenges.times[2].start}:R>\nEnds <t:{challenges.times[2].end}:F> <t:{challenges.times[2].end}:R>\n
                                Starts <t:{challenges.times[3].start}:F> <t:{challenges.times[3].start}:R>\nEnds <t:{challenges.times[3].end}:F> <t:{challenges.times[3].end}:R>\n
                                Starts <t:{challenges.times[4].start}:F> <t:{challenges.times[4].start}:R>\nEnds <t:{challenges.times[4].end}:F> <t:{challenges.times[4].end}:R>\n
                                Starts <t:{challenges.times[5].start}:F> <t:{challenges.times[5].start}:R>\nEnds <t:{challenges.times[5].end}:F> <t:{challenges.times[5].end}:R>''', 
                                inline = False)
        
        challenge_one.set_image(url = challenges.maps[0].image)
        challenge_one.set_footer(text = challenges.maps[0].name)

        challenge_two = discord.Embed(color = discord.Color.from_rgb(244, 79, 148))
        challenge_two.set_image(url = challenges.maps[1].image)
        challenge_two.set_footer(text = challenges.maps[1].name)

        return challenge_one, challenge_two

    async def salmon_run(self, node: int) -> discord.Embed | None:
        '''
        Returns Salmon Run information in an embed
        '''
        nodes = self.schedules
        try:
            salmon_run_info = nodes.SalmonRun[node]

        except IndexError:
            return None
        
        salmon_info = SalmonRun(times = TimeSlots(
            start = await self.generate_timestamp(salmon_run_info['startTime']),
            end = await self.generate_timestamp(salmon_run_info['endTime'])
            ),
            stage = Stage(
                name = salmon_run_info['setting']['coopStage']['name'],
                image = salmon_run_info['setting']['coopStage']['image']['url']
                ),
                weapons = [salmon_run_info['setting']['weapons'][i]['name'] for i in range(4)],
                boss = salmon_run_info['setting']['boss']['name'])


        salmon_run = discord.Embed(title = 'Salmon Run', description = f'Start time: <t:{salmon_info.times.start}:f>, <t:{salmon_info.times.start}:R>\nEnd Time: <t:{salmon_info.times.end}:f>, <t:{salmon_info.times.end}:R>', color = discord.Color.purple())
        salmon_run.add_field(name = f"{salmon_info.stage.name} - {salmon_info.boss}", value = '\n'.join(weapon for weapon in salmon_info.weapons))
        salmon_run.set_image(url = salmon_info.stage.image)
        salmon_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')
        salmon_run.set_footer(text = 'Powered by **Splatoon3.ink**')

        return salmon_run

    async def big_run(self) -> discord.Embed | None:
        '''
        Returns Big Run information
        '''

        schedule = self.schedules

        try:
            big_run_info = schedule['coopGroupingSchedule']['bigRunSchedule']['nodes'][0]
        
        except IndexError:
            return None
        
        start, end = await self.generate_timestamp(big_run_info['startTime'], big_run_info['endTime'])

        maps = big_run_info['setting']['coopStage']
        weapons = big_run_info['setting']['weapons']
        king_salmonid = big_run_info['__splatoon3ink_king_salmonid_guess']

        big_run = discord.Embed(title = 'Big Run', description = f'Start time: <t:{start}:f>, <t:{start}:R>\nEnd Time: <t:{end}:f>, <t:{end}:R>', color = discord.Color.purple())
        big_run.add_field(name = f"{maps['name']} - {king_salmonid}", value = '\n'.join(node['name'] for node in weapons))
        big_run.set_image(url = maps['image']['url'])
        big_run.set_thumbnail(url = 'https://cdn.wikimg.net/en/splatoonwiki/images/thumb/9/98/S3_Icon_Big_Run.svg/1200px-S3_Icon_Big_Run.svg.png')
        big_run.set_footer(text = 'Powered by **Splatoon3.ink**')

        return big_run
    
    async def eggstra_work(self) -> discord.Embed | None:
        ...
    
    async def splatfest(self, node: int) -> discord.Embed | None:
        ...

            
    @app_commands.command(name = 's3_maps', description = 'Displays the current rotations for Splatoon 3')
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = 'All'):
        mode = mode.title().strip()

        match mode:
            case 'All':
                rotation_update = await self.s3_rotation_update(0)
                turf_war_one, turf_war_two = await self.turf_war(0)
                anarchy_series_one, anarchy_series_two = await self.anarchy_series(0)
                anarchy_open_one, anarchy_open_two = await self.anarchy_open(0)
                challenge_one, challenge_two = await self.challenges(0)

                await interaction.response.send_message(embeds = [rotation_update, turf_war_one, turf_war_two, anarchy_series_one, anarchy_series_two, anarchy_open_one, anarchy_open_two, challenge_one, challenge_two])
            
            case 'Turf War':
                rotation_update = await self.s3_rotation_update(0)
                turf_war_one, turf_war_two = await self.turf_war(0)
                await interaction.response.send_message(embeds = [rotation_update, turf_war_one, turf_war_two])

            case 'Anarchy Series':
                rotation_update = await self.s3_rotation_update(0)
                anarchy_series_one, anarchy_series_two = await self.anarchy_series(0)
                await interaction.response.send_message(embeds = [rotation_update, anarchy_series_one, anarchy_series_two])

            case 'Anarchy Open':
                rotation_update = await self.s3_rotation_update(0)
                anarchy_open_one, anarchy_open_two = await self.anarchy_open(0)
                await interaction.response.send_message(embeds = [rotation_update, anarchy_open_one, anarchy_open_two])
            
            case 'Challenge':
                challenge_one, challenge_two = await self.challenges(0)
                if challenge_one:
                    await interaction.response.send_message(embeds = [challenge_one, challenge_two])
                
                else:
                    await interaction.response.send_message(content = 'There aren\'t any challenges on the horizon', ephemeral = True)
            
            case 'Salmon Run':
                salmon_run = await self.salmon_run(0)
                await interaction.response.send_message(embed = salmon_run)

            case _:
                await interaction.response.send_message(content = 'That is not a valid game mode', ephemeral = True)

    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'Challenge', 'Salmon Run']
        return [app_commands.Choice(name = mode, value = mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel_id: int) -> None:

        channel = self.bot.get_channel(channel_id)
        await channel.purge()
        await asyncio.sleep(1)

        rotation_update = await self.s3_rotation_update(0)
        future_rotation_update = await self.s3_rotation_update(1)

        current = ModeEmbeds(
            turf_war = await self.turf_war(0),
            anarchy_series = await self.anarchy_series(0),
            anarchy_open = await self.anarchy_open(0),
            x_battle = await self.x_battles(0),
            salmon_run = await self.salmon_run(0),
            challenge = await self.challenges(0),
            big_run = None,
            eggstra_work = None
        )

        future = ModeEmbeds(
            turf_war = await self.turf_war(1),
            anarchy_series = await self.anarchy_series(1),
            anarchy_open = await self.anarchy_open(1),
            x_battle = await self.x_battles(1),
            salmon_run = await self.salmon_run(1),
            challenge = await self.challenges(1),
            big_run = None,
            eggstra_work = None
        )

        current_modes = [mode for modes in [current.turf_war, current.anarchy_series, current.anarchy_open, current.x_battle, current.challenge] if modes is not None for mode in modes]
        future_modes = [mode for modes in [future.turf_war, future.anarchy_series, future.anarchy_open, future.x_battle, future.challenge] if modes is not None for mode in modes]
        
        gamemodes = list(filter(lambda mode: mode is not None, current_modes))
        salmon_run_stuff = list(filter(lambda mode: mode is not None, [current.salmon_run, current.big_run, current.eggstra_work]))
        future_gamemodes = list(filter(lambda mode: mode is not None, future_modes))
        future_salmon_stuff = list(filter(lambda mode: mode is not None, [future.salmon_run, future.big_run, future.eggstra_work]))

        await channel.send(embed = rotation_update)
        await channel.send(embeds = gamemodes)
        await channel.send(embeds = salmon_run_stuff)

        await channel.send(content = '------------------------------------------------')

        await channel.send(embed = future_rotation_update)
        await channel.send(embeds = future_gamemodes)
        await channel.send(embeds = future_salmon_stuff)
    
    @tasks.loop(seconds = 10)
    async def embed_send(self):
        await self.api_call()
        await self.channel_setup(1088459539147411497)
        await self.channel_setup(1089292971033235466)
        
        self.embed_send.change_interval(time = time_calc())

    @embed_send.before_loop
    async def before_embed_send_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(maps_modes(bot))