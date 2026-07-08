from pydantic import BaseModel, Field, AwareDatetime, AliasPath, BeforeValidator, AfterValidator, HttpUrl, ConfigDict
from typing import Optional, Annotated
from discord import User, Embed, File


class Stage(BaseModel):
    name: str
    image_url: Annotated[HttpUrl, Field(validation_alias=AliasPath('image', 'url'))]

class SRWeapon(BaseModel):
    weapon: Annotated[str, Field(alias='name')]
    image_url: Annotated[HttpUrl, Field(validation_alias=AliasPath('image', 'url'))]

class TimeSlots(BaseModel):
    start: Annotated[AwareDatetime, Field(alias='startTime')]
    end: Annotated[AwareDatetime, Field(alias='endTime')]

class PvP(TimeSlots):
    maps: list[Stage]
    gamemode: str
    rule: Optional[str] = None
    fest_active: Annotated[bool, Field(alias='festMatchSettings'), BeforeValidator(lambda x: bool(x))] = False

class PvE(TimeSlots):
    stage: Stage
    weapons: list[SRWeapon]
    boss: Optional[str] = None
    mode_image: HttpUrl

class TurfWar(PvP):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('regularMatchSetting', 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('regularMatchSetting', 'vsRule', 'name'))]
    rule: Annotated[Optional[str], Field(validation_alias=AliasPath('regularMatchSetting', 'vsRule', 'rule'))] = None

class Ranked(PvP):
    maps: list[Stage]
    gamemode: str
    rule: str

class Series(Ranked):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('bankaraMatchSettings', 0, 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('bankaraMatchSettings', 0, 'vsRule', 'name'))] = None
    rule: Annotated[Optional[str], Field(validation_alias=AliasPath('bankaraMatchSettings', 0, 'vsRule', 'rule'))] = None

class Open(Ranked):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('bankaraMatchSettings', 1, 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('bankaraMatchSettings', 1, 'vsRule', 'name'))] = None
    rule: Annotated[Optional[str], Field(validation_alias=AliasPath('bankaraMatchSettings', 1, 'vsRule', 'rule'))] = None

class XBattles(Ranked):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('xMatchSetting', 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('xMatchSetting', 'vsRule', 'name'))] = None
    rule: Annotated[Optional[str], Field(validation_alias=AliasPath('xMatchSetting', 'vsRule', 'rule'))] = None

class SalmonRun(PvE):
    stage: Annotated[Stage, Field(validation_alias=AliasPath('setting', 'coopStage'))]
    weapons: Annotated[list[SRWeapon], Field(validation_alias=AliasPath('setting', 'weapons'))]
    boss: Annotated[str, Field(validation_alias=AliasPath('setting', 'boss', 'name'))]
    mode_image: HttpUrl = 'https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png'

class Challenge(PvP):
    start: AwareDatetime = None
    end: AwareDatetime = None
    title: Annotated[Optional[str], Field(validation_alias=AliasPath('leagueMatchSetting', 'leagueMatchEvent', 'name'))] = None
    description: Annotated[Optional[str], Field(validation_alias=AliasPath('leagueMatchSetting', 'leagueMatchEvent', 'desc')), AfterValidator(lambda x: x.replace('<br />', ' '))] = None
    extended_description: Annotated[Optional[str], Field(validation_alias=AliasPath('leagueMatchSetting', 'leagueMatchEvent','regulation')), AfterValidator(lambda x: x.replace('<br />', '\n').replace('・', ''))] = None
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('leagueMatchSetting', 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('leagueMatchSetting', 'vsRule', 'name'))] = None
    rule: Annotated[Optional[str], Field(validation_alias=AliasPath('leagueMatchSetting', 'vsRule', 'rule'))] = None
    time: Annotated[Optional[list[TimeSlots]], Field(alias='timePeriods')] = None

class BigRun(PvE):
    stage: Annotated[Stage, Field(validation_alias=AliasPath('setting', 'coopStage'))]
    weapons: Annotated[list[SRWeapon], Field(validation_alias=AliasPath('setting', 'weapons'))]
    boss: Annotated[str, Field(validation_alias=AliasPath('setting', 'boss', 'name'))]
    mode_image: HttpUrl = 'https://cdn.wikimg.net/en/splatoonwiki/images/thumb/9/98/S3_Icon_Big_Run.svg/1200px-S3_Icon_Big_Run.svg.png'

class EggstraWork(PvE):
    stage: Annotated[Stage, Field(validation_alias=AliasPath('setting', 'coopStage'))]
    weapons: Annotated[list[str], Field(validation_alias=AliasPath('setting', 'weapons'))]
    mode_image: HttpUrl = 'https://cdn.wikimg.net/en/splatoonwiki/images/thumb/7/77/S3_Icon_Eggstra_Work.svg/120px-S3_Icon_Eggstra_Work.svg.png?20230220215341'

class Splatfest(PvP):
    maps: Optional[list[Stage]] = None
    gamemode: Optional[str] = None

class SplatfestOpen(Splatfest):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('festMatchSettings', 1, 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('festMatchSettings', 1, 'vsRule', 'name'))] = None

class SplatfestPro(Splatfest):
    maps: Annotated[Optional[list[Stage]], Field(validation_alias=AliasPath('festMatchSettings', 0, 'vsStages'))] = None
    gamemode: Annotated[Optional[str], Field(validation_alias=AliasPath('festMatchSettings', 0, 'vsRule', 'name'))] = None

class Tricolor(PvP):                                                                    # come back to this. Fields, not properly known how to define
    start: Annotated[AwareDatetime, Field(alias='midtermTime')]
    maps: Annotated[list[Stage], Field(alias='tricolorStages')]
    is_available: Annotated[bool, Field(alias='state'), BeforeValidator(lambda x: True if x == 'SECOND_HALF' else False)]

class ScheduleResponse(BaseModel):
    turf_war: Annotated[Optional[list[TurfWar]], Field(validation_alias=AliasPath('data', 'regularSchedules', 'nodes'))] = None
    anarchy_series: Annotated[Optional[list[Series]], Field(validation_alias=AliasPath('data', 'bankaraSchedules', 'nodes'))] = None
    anarchy_open: Annotated[Optional[list[Open]], Field(validation_alias=AliasPath('data', 'bankaraSchedules', 'nodes'))] = None
    salmon_run: Annotated[Optional[list[SalmonRun]], Field(validation_alias=AliasPath('data', 'coopGroupingSchedule', 'regularSchedules', 'nodes'))] = None
    challenge: Annotated[Optional[list[Challenge]], Field(validation_alias=AliasPath('data', 'eventSchedules', 'nodes'))] = None
    x_battles: Annotated[Optional[list[XBattles]], Field(validation_alias=AliasPath('data', 'xSchedules', 'nodes'))] = None
    big_run: Annotated[Optional[list[BigRun]], Field(validation_alias=AliasPath('data', 'coopGroupingSchedule', 'bigRunSchedules', 'nodes'))] = None
    eggstra_work: Annotated[Optional[list[EggstraWork]], Field(validation_alias=AliasPath('data', 'coopGroupingSchedule', 'teamContestSchedules', 'nodes'))] = None
    splatfest_open: Annotated[Optional[list[SplatfestOpen]], Field(validation_alias=AliasPath('data', 'festSchedules', 'nodes'))] = None
    splatfest_pro: Annotated[Optional[list[SplatfestPro]], Field(validation_alias=AliasPath('data', 'festSchedules', 'nodes'))] = None
    tricolor_battles: Annotated[Optional[list[Tricolor]], Field(validation_alias=AliasPath('data', 'currentFest'))] = None

class ProcessedReturns(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    embed: Embed
    file: Optional[File] = None

class Teams(BaseModel):
    name: Annotated[str, Field(alias='teamName')]
    team_image: Annotated[HttpUrl, Field(validation_alias=AliasPath('image', 'url'))]

class FestivalsResponse(TimeSlots):
    id: Annotated[str, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'id'))]
    start: Annotated[AwareDatetime, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'startTime'))]
    end: Annotated[AwareDatetime, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'endTime'))]
    title: Annotated[str, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'title'))]
    image_url: Annotated[HttpUrl, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'image', 'url'))]
    teams: Annotated[list[Teams], Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'teams'))]
    state: Annotated[str, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'state'))]
    is_votable: Annotated[bool, Field(validation_alias=AliasPath('US', 'data', 'festRecords', 'nodes', 0, 'isVotable'))]

class Votes(BaseModel):
    team_name: str
    members: list[User] = []
    model_config = ConfigDict(arbitrary_types_allowed=True)
