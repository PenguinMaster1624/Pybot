from pydantic import BaseModel, ConfigDict
from discord import Embed, File

class ApiResponse(BaseModel):
    TurfWar: list[dict]
    Anarchy: list[dict]
    SalmonRun: list[dict]
    Challenge: list[dict]
    XBattles: list[dict]
    BigRun: list[dict]
    EggstraWork: list[dict]
    Splatfest: list[dict]
    Tricolor: dict | None

class Stage(BaseModel):
    name: str
    image: str

class TimeSlots(BaseModel):
    start: int
    end: int

class TurfWar(BaseModel):
    times: TimeSlots
    maps: list[Stage] | None
    fest_active: bool

class Ranked(BaseModel):
    times: TimeSlots
    maps: list[Stage] | None
    gamemode: str | None
    fest_active: bool

class SalmonRun(BaseModel):
    times: TimeSlots
    stage: Stage
    weapons: list[str]
    boss: str

class Challenge(BaseModel):
    title: str
    description: str
    extended_description: str
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

class Splatfest(BaseModel): 
    times: TimeSlots
    maps: list[Stage] | None
    mode: str | None
    fest_active: bool

class Tricolor(BaseModel):
    availability: TimeSlots
    stage: Stage
    is_available: bool

class GameModes(BaseModel):
    turf_war: TurfWar | None
    anarchy_series: Ranked | None
    anarchy_open: Ranked | None
    x_battles: Ranked | None
    salmon_run: SalmonRun | None
    challenge: Challenge | None
    big_run: BigRun | None
    eggstra_work: EggstraWork | None
    splatfest_open: Splatfest | None
    splatfest_pro: Splatfest | None
    tricolor_battle: Tricolor | None

class ModeEmbeds(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)

    turf_war: list[Embed | File] | None
    anarchy_series: list[Embed | File] | None
    anarchy_open: list[Embed | File] | None
    x_battle: list[Embed | File] | None
    salmon_run: Embed | None
    challenge: list[Embed | File] | None
    big_run: Embed | None
    eggstra_work: Embed | None
    splatfest_open: list[Embed | File] | None
    splatfest_pro: list[Embed | File] | None
    tricolor_battle: Embed | None