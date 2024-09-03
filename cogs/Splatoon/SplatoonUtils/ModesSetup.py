from .SplatoonUtils import generate_timestamp
from .GameModeClasses import *
import aiohttp


class MapsModesSetup:
    def __init__(self) -> None:
        '''Used to set up game mode
        classes for Splatoon 3 Maps and Modes
        '''
        self.gamemodes: list[GameModes] | None = None
    

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
                                 Splatfest = js['festSchedules']['nodes'],
                                 Tricolor = js['currentFest']
            )

            self.response = modes

    async def turf_war(self, node: int) -> TurfWar | None:
        mode = self.response.TurfWar

        try:
            turf_war = mode[node]
            
        except IndexError:
            return None
        
        turf_info = TurfWar(times = TimeSlots(start = await generate_timestamp(turf_war['startTime']), end = await generate_timestamp(turf_war['endTime'])),
                            maps = [Stage(name = turf_war['regularMatchSetting']['vsStages'][stage]['name'], image = turf_war['regularMatchSetting']['vsStages'][stage]['image']['url']) for stage in range(2)] if turf_war['regularMatchSetting'] else None,
                            fest_active = True if turf_war['festMatchSettings'] else False)
        
        return turf_info


    async def anarchy_series(self, node: int) -> Ranked | None:
        mode = self.response.Anarchy
        info = mode[node]

        try:
            anarchy_series = mode[node]['bankaraMatchSettings'][0]
        
        except TypeError:
            return None

        series_info = Ranked(times = TimeSlots(start = await generate_timestamp(mode[node]['startTime']),  end = await generate_timestamp(mode[node]['endTime'])), 
                                    maps = [Stage(name = anarchy_series['vsStages'][stage]['name'], image = anarchy_series['vsStages'][stage]['image']['url']) for stage in range(2)] if anarchy_series else None,
                                    fest_active = True if info['festMatchSettings'] else False,
                                    gamemode = anarchy_series['vsRule']['name'])
        
        return series_info
    

    async def anarchy_open(self, node: int) -> Ranked | None:
        mode = self.response.Anarchy
        info = mode[node]

        try:
            anarchy_open = mode[node]['bankaraMatchSettings'][1]

        except TypeError:
            return None
        
        series_info = Ranked(times = TimeSlots(start = await generate_timestamp(mode[node]['startTime']), end = await generate_timestamp(mode[node]['endTime'])), 
                                    maps = [Stage(name = anarchy_open['vsStages'][stage]['name'],image = anarchy_open['vsStages'][stage]['image']['url']) for stage in range(2)] if anarchy_open else None,
                                    fest_active = True if info['festMatchSettings'] else False,
                                    gamemode = anarchy_open['vsRule']['name'])
        
        return series_info
    

    async def x_battles(self, node: int) -> Ranked | None:
        mode = self.response.XBattles

        try:
            x_battles = mode[node]['xMatchSetting']
        
        except IndexError:
            return None
        
        x_info = Ranked(times = TimeSlots(start = await generate_timestamp(mode[node]['startTime']), end = await generate_timestamp(mode[node]['endTime'])), 
                        maps = [Stage(name = x_battles['vsStages'][stage]['name'], image = x_battles['vsStages'][stage]['image']['url']) for stage in range(2)] if x_battles else None, 
                        fest_active = True if mode[node]['festMatchSettings'] else False,
                        gamemode = x_battles['vsRule']['name'] if x_battles else None)
        
        return x_info
    

    async def challenges(self, node: int) -> Challenge | None:
        mode = self.response.Challenge

        try:
            challenges_info = mode[node]
            
        except TypeError | IndexError:
            return None
        
        challenges_timeslots = challenges_info['timePeriods']
        challenges_info = challenges_info['leagueMatchSetting']            
        challenge_maps = challenges_info['vsStages']

        regulation = str(challenges_info['leagueMatchEvent']['regulation']).split('<br />')
        processed_regulation = '\n'.join(i.strip('・ ') for i in regulation)

        desc = str(challenges_info['leagueMatchEvent']['desc']).split('<br />')
        processed_desc = '\n'.join(i.strip('・ ') for i in desc)

        challenges = Challenge(title = challenges_info['leagueMatchEvent']['name'],
                               description = processed_desc,
                               extended_description = processed_regulation,
                               times = [TimeSlots(start = await generate_timestamp(challenges_timeslots[slot]['startTime']), end = await generate_timestamp(challenges_timeslots[slot]['endTime'])) for slot, data in enumerate(challenges_timeslots)],
                               maps = [Stage(name = challenge_maps[stage]['name'], image = challenge_maps[stage]['image']['url']) for stage in range(2)],
                               gamemode = challenges_info['vsRule']['name'])
        
        return challenges
    

    async def salmon_run(self, node: int) -> SalmonRun | None:
        mode = self.response.SalmonRun

        try:
            salmon_run = mode[node]

        except IndexError:
            return None
        
        salmon_info = SalmonRun(times = TimeSlots(
            start = await generate_timestamp(salmon_run['startTime']), end = await generate_timestamp(salmon_run['endTime'])),
            stage = Stage(
                name = salmon_run['setting']['coopStage']['name'], image = salmon_run['setting']['coopStage']['image']['url']),
                weapons = [salmon_run['setting']['weapons'][i]['name'] for i in range(4)],
                boss = salmon_run['setting']['boss']['name']
                )
        
        return salmon_info
    

    async def big_run(self) -> BigRun | None:
        mode = self.response.BigRun

        try:
            big_run = mode[0]
            
        except IndexError:
            return None
                
        big_run_info = BigRun(time = TimeSlots(start = await generate_timestamp(big_run['startTime']), end = await generate_timestamp(big_run['endTime'])),
                              stage = Stage(name = big_run['setting']['coopStage']['name'], image = big_run['setting']['coopStage']['image']['url']),
                              weapons =  [big_run['setting']['weapons'][i]['name'] for i in range(4)],
                              boss = big_run['setting']['boss']['name'])
        
        return big_run_info


    async def eggstra_work(self) -> EggstraWork | None:
        mode = self.response.EggstraWork

        try:
            eggstra_work = mode[0]

        except IndexError:
            return None
        
        eggstra_work_info = EggstraWork(time = TimeSlots(start = await generate_timestamp(eggstra_work['startTime']), end = await generate_timestamp(eggstra_work['endTime'])),
                                        stage = Stage(name = eggstra_work['setting']['coopStage']['name'], image = eggstra_work['setting']['coopStage']['image']['url']),
                                        weapons = [eggstra_work['setting']['weapons'][weapon]['name'] for weapon in range(4)])
        
        return eggstra_work_info

    async def splatfest_pro(self, node: int) -> Splatfest | None:
        mode = self.response.Splatfest

        try:
            splatfest = mode[node]
            
        except IndexError:
            return None
        
        mode_info = splatfest['festMatchSettings']

        splatfest_info = Splatfest(times = TimeSlots(start = await generate_timestamp(splatfest['startTime']), end = await generate_timestamp(splatfest['endTime'])),
                            maps = [Stage(name = mode_info[0]['vsStages'][stage]['name'], image = mode_info[0]['vsStages'][stage]['image']['url']) for stage in range(2)] if mode_info else None,
                            mode = 'Pro' if mode_info else None,
                            fest_active = False if mode_info is None else True)
        
        return splatfest_info
    

    async def splatfest_open(self, node: int) -> Splatfest | None:
        mode = self.response.Splatfest

        try:
            splatfest = mode[node]
            
        except IndexError:
            return None
        
        mode_info = splatfest['festMatchSettings']

        splatfest_info = Splatfest(times = TimeSlots(start = await generate_timestamp(splatfest['startTime']), end = await generate_timestamp(splatfest['endTime'])),
                            maps = [Stage(name = mode_info[1]['vsStages'][stage]['name'], image = mode_info[1]['vsStages'][stage]['image']['url']) for stage in range(2)] if mode_info else None,
                            mode = 'Open' if mode_info else None,
                            fest_active = False if mode_info is None else True)
        
        return splatfest_info
    
    async def tricolor_battle(self) -> Tricolor | None:
        if (mode := self.response.Tricolor) is None:
            return None
        
        stage_info = mode['tricolorStage']
        tricolor_info = Tricolor(availability = TimeSlots(start = await generate_timestamp(mode['midtermTime']), end = await generate_timestamp(mode['endTime'])),
                                 stage = Stage(name = stage_info['name'], image = stage_info['image']['url']),
                                 is_available = True if mode['state'] == 'SECOND_HALF' else False)
        
        return tricolor_info
    
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
                big_run = await self.big_run(), 
                eggstra_work = await self.eggstra_work(),
                splatfest_open = await self.splatfest_open(node),
                splatfest_pro = await self.splatfest_pro(node),
                tricolor_battle = await self.tricolor_battle()
                ) for node in nodes]
        