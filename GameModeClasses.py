from pydantic import BaseModel, ConfigDict
from discord import Embed

class ApiResponse(BaseModel):
    TurfWar: list | None
    Anarchy: list | None
    SalmonRun: list[dict] | None
    Challenge: list | None
    XBattles: list | None
    BigRun: dict | None
    EggstraWork: dict | None

class Stage(BaseModel):
    name: str
    image: str

class TimeSlots(BaseModel):
    start: int
    end: int

class TurfWar(BaseModel):
    times: TimeSlots
    maps: list[Stage]

class Ranked(BaseModel):
    times: TimeSlots
    maps: list[Stage]
    gamemode: str

class SalmonRun(BaseModel):
    times: TimeSlots
    stage: Stage
    weapons: list[str]
    boss: str

class Challenge(BaseModel):
    title: str
    description: str
    times: list[TimeSlots]
    maps: list[Stage]
    gamemode: str

class BigRun(BaseModel):
    time: TimeSlots
    stage: Stage
    weapons: list[str]
    boss: str

class EggstraWork(BaseModel):
    time: TimeSlots
    stage: Stage
    weapons: list[str]
    boss: str

class Splatfest(BaseModel):
    times: TimeSlots
    maps: list[Stage]

class GameModes(BaseModel):
    turf_war: TurfWar | None
    anarchy_series: Ranked | None
    anarchy_open: Ranked | None
    x_battles: Ranked | None
    salmon_run: SalmonRun | None
    challenge: Challenge | None
    big_run: BigRun | None
    eggstra_work: EggstraWork | None

class ModeEmbeds(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)

    turf_war: list[Embed] | None
    anarchy_series: list[Embed] | None
    anarchy_open: list[Embed] | None
    x_battle: list[Embed] | None
    salmon_run: Embed | None
    challenge: list[Embed] | None
    big_run: Embed | None
    eggstra_work: Embed | None
