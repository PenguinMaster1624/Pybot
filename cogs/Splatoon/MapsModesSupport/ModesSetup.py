from .GameModeClasses import *
from zoneinfo import ZoneInfo
import datetime
import aiohttp


class MapsModesSetup:
    def __init__(self) -> None:
         '''Used to set up game mode
       classes for Splatoon 3 Maps and Modes
       '''
         self.response = None
         self.gamemodes: list[GameModes] | None = None

    async def generate_timestamp(self, time: str) -> str:
        '''
        Generates a timestamp as a string for use in Discord Embeds
        '''
        new_time = str(datetime.datetime.fromisoformat(time[:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
        return new_time
    
    async def api_call(self) -> None:
       async with aiohttp.ClientSession() as session:
           async with session.get('https://splatoon3.ink/data/schedules.json') as response: 
            js = await response.json() 
            js = js['data'] 
            modes = ApiResponse(TurfWar = js['regularSchedules']['nodes'], 
                                 Anarchy = js['bankaraSchedules']['nodes'], 
                                 SalmonRun = js['coopGroupingSchedule']['regularSchedules']['nodes'],
                                 Challenge = js['eventSchedules']['nodes'], 
                                 XBattles = js['xSchedules']['nodes'],
                                 BigRun = js['coopGroupingSchedule']['bigRunSchedules']['nodes'],
                                 EggstraWork = js['coopGroupingSchedule']['teamContestSchedules']['nodes'],
                                 Splatfest = js['festSchedules']['nodes']
            )

            self.response = modes

    async def turf_war(self, node: int) -> TurfWar | None:
        mode = self.response.TurfWar

        try:
            turf_war = mode[node]
            
        except IndexError:
            return None
        
        turf_info = TurfWar(times = TimeSlots(start = await self.generate_timestamp(turf_war['startTime']), end = await self.generate_timestamp(turf_war['endTime'])),
                            maps = [Stage(name = turf_war['regularMatchSetting']['vsStages'][stage]['name'], image = turf_war['regularMatchSetting']['vsStages'][stage]['image']['url']) for stage in range(2)])
        
        return turf_info


    async def anarchy_series(self, node: int) -> Ranked | None:
        mode = self.response.Anarchy

        try:
            anarchy_series = mode[node]['bankaraMatchSettings'][0]
        
        except IndexError:
            return None

        series_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(mode[node]['startTime']),  end = await self.generate_timestamp(mode[node]['endTime'])), 
                                    maps = [Stage(name = anarchy_series['vsStages'][stage]['name'], image = anarchy_series['vsStages'][stage]['image']['url']) for stage in range(2)],
                                    gamemode = anarchy_series['vsRule']['name'])
        
        return series_info
    

    async def anarchy_open(self, node: int) -> Ranked | None:
        mode = self.response.Anarchy

        try:
            anarchy_series = mode[node]['bankaraMatchSettings'][1]

        except IndexError:
            return None
        
        series_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(mode[node]['startTime']), end = await self.generate_timestamp(mode[node]['endTime'])), 
                                    maps = [Stage(name = anarchy_series['vsStages'][stage]['name'],image = anarchy_series['vsStages'][stage]['image']['url']) for stage in range(2)],
                                    gamemode = anarchy_series['vsRule']['name'])
        
        return series_info
    
    async def x_battles(self, node: int) -> Ranked | None:
        mode = self.response.XBattles

        try:
            x_battles = mode[node]['xMatchSetting']
        
        except IndexError:
            return None

        x_info = Ranked(times = TimeSlots(start = await self.generate_timestamp(mode[node]['startTime']), end = await self.generate_timestamp(mode[node]['endTime'])), 
                        maps = [Stage(name = x_battles['vsStages'][stage]['name'], image = x_battles['vsStages'][stage]['image']['url']) for stage in range(2)], 
                        gamemode = x_battles['vsRule']['name'])
        
        return x_info
    

    async def challenges(self, node: int) -> Challenge | None:
        mode = self.response.Challenge

        try:
            challenges_info = mode[node]
            challenges_timeslots = challenges_info['timePeriods']
            challenges_info = challenges_info['leagueMatchSetting']
            challenge_maps = challenges_info['vsStages']


        except IndexError:
            return None
        
        regulation = str(challenges_info['leagueMatchEvent']['regulation']).split('<br />')
        regulation = '\n'.join(i.strip('・ ') for i in regulation)

        desc = str(challenges_info['leagueMatchEvent']['desc']).split('<br />')
        desc = '\n'.join(i.strip('・ ') for i in desc)

        challenges = Challenge(title = challenges_info['leagueMatchEvent']['name'],
                               description = desc,
                               extended_description = regulation,
                               times = [TimeSlots(start = await self.generate_timestamp(challenges_timeslots[slot]['startTime']), end = await self.generate_timestamp(challenges_timeslots[slot]['endTime'])) for slot, data in enumerate(challenges_timeslots)],
                               maps = [Stage(name = challenge_maps[stag]['name'], image = challenge_maps[stag]['image']['url']) for stag in range(2)],
                               gamemode = challenges_info['vsRule']['name'])
        
        return challenges
    

    async def salmon_run(self, node: int) -> SalmonRun | None:
        mode = self.response.SalmonRun

        try:
            salmon_run = mode[node]

        except IndexError:
            return None
        
        salmon_info = SalmonRun(times = TimeSlots(
            start = await self.generate_timestamp(salmon_run['startTime']), end = await self.generate_timestamp(salmon_run['endTime'])),
            stage = Stage(
                name = salmon_run['setting']['coopStage']['name'], image = salmon_run['setting']['coopStage']['image']['url']),
                weapons = [salmon_run['setting']['weapons'][i]['name'] for i in range(4)],
                boss = salmon_run['setting']['boss']['name']
                )
        
        return salmon_info
    

    async def big_run(self) -> BigRun | None:
        return
        
        try:
            big_run_info = schedule['coopGroupingSchedule']['bigRunSchedule']['nodes'][0]
        
        except IndexError:
            return None
        
        start, end = await self.generate_timestamp(big_run_info['startTime'], big_run_info['endTime'])

        maps = big_run_info['setting']['coopStage']
        weapons = big_run_info['setting']['weapons']
        king_salmonid = big_run_info['__splatoon3ink_king_salmonid_guess']


    async def eggstra_work(self) -> EggstraWork | None:
        return
    

    async def splatfest(self, node: int) -> Splatfest | None:
        mode = self.response.Splatfest

        try:
            splatfest = mode[node]
            
        except IndexError:
            return None
        
        splatfest_info = Splatfest(times = TimeSlots(start = await self.generate_timestamp(splatfest['startTime']), end = await self.generate_timestamp(splatfest['endTime'])),
                            maps = [Stage(name = splatfest['regularMatchSetting']['vsStages'][stage]['name'], image = splatfest['regularMatchSetting']['vsStages'][stage]['image']['url']) for stage in range(2)],
                            fest_active = splatfest['festMatchSettings'])
        
        return splatfest_info

    
    async def gather(self, nodes: list[int]) -> None:
        await self.api_call()
        self.gamemodes = [
            GameModes(
                turf_war = await self.turf_war(node), 
                anarchy_series = await self.anarchy_series(node), 
                anarchy_open = await self.anarchy_open(node), 
                x_battles = await self.x_battles(node), 
                salmon_run = await self.salmon_run(node), 
                challenge = await self.challenges(node), 
                big_run = None, 
                eggstra_work = None,
                splatfest = await self.splatfest(node)
                ) for node in nodes]
        