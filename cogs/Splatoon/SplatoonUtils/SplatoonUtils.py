from zoneinfo import ZoneInfo
import datetime

async def generate_timestamp(time: str) -> int:
    '''
    Generates a timestamp as a string for use in Discord Embeds
    '''
    time = str(datetime.datetime.fromisoformat(time[:-1]).replace(tzinfo = ZoneInfo('UTC')).timestamp())[:-2]
    new_time = int(time)
    
    return new_time