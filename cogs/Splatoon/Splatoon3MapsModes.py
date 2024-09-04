from .SplatoonUtils.GameModeClasses import TurfWar, Ranked, Splatfest, SalmonRun, ModeEmbeds
from .SplatoonUtils.ModesSetup import MapsModesSetup
from discord.ext import commands, tasks
from discord import app_commands
from zoneinfo import ZoneInfo
from io import BytesIO
from PIL import Image
import requests
import asyncio
import datetime
import discord
import json


def time_calc() -> datetime.time:
    response = requests.get('https://splatoon3.ink/data/schedules.json')

    if response.status_code == 200:
        js = response.json()
        js = js['data']

        try:
            time = js['regularSchedules']['nodes'][0]

        except KeyError:
            time = js['festSchedules']['nodes'][0]

        end = datetime.datetime.fromisoformat(time['endTime'][:-1]).replace(tzinfo=ZoneInfo('UTC'))

        return datetime.time(hour=end.hour, minute=end.minute, second=30, tzinfo=ZoneInfo('UTC'))


class maps_modes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.embed_send.start()
        self.modes = None


    async def image_create(self, mode: TurfWar | Ranked | Splatfest, filename: str) -> discord.File:
        '''
        Creates Discord File objects to use in other functions
        '''
        stage_one = Image.open(BytesIO(requests.get(mode.maps[0].image).content))
        stage_two = Image.open(BytesIO(requests.get(mode.maps[1].image).content))
        
        merged = Image.new('RGB', (stage_one.width + stage_two.width, stage_one.height))
        merged.paste(stage_one, (0, 0))
        merged.paste(stage_two, (stage_one.width, 0))

        final = BytesIO()
        merged.save(final, format='PNG')
        final.seek(0)

        return discord.File(fp=final, filename=f'{filename}.png')


    async def api_call(self) -> None:
        '''
        Gathers the necessary information for the embeds
        '''

        modes = MapsModesSetup()
        await modes.gather([0, 1])
        self.modes = modes.gamemodes


    async def s3_rotation_update(self, mode: TurfWar | Ranked | Splatfest | SalmonRun) -> str:
        rotation_update = f'Start Time: <t:{mode.times.start}:t>, <t:{mode.times.start}:R>\nEnd Time: <t:{mode.times.end}:t>, <t:{mode.times.end}:R>'
        return rotation_update


    async def turf_war(self, node: int) -> discord.Embed | discord.File | None:
        '''
        Returns Splatoon 3 Turf War information
        '''

        turf_info = self.modes[node].turf_war

        if turf_info.fest_active is True:
            return None

        file = await self.image_create(turf_info, 'turf_war')
        time = await self.s3_rotation_update(turf_info)

        turf_war = discord.Embed(color=discord.Color.green())
        turf_war.add_field(name='Turf War', value=time)
        turf_war.set_image(url='attachment://turf_war.png')
        turf_war.set_footer(text=f'{turf_info.maps[0].name} | {turf_info.maps[1].name}')


        return [turf_war, file]


    async def anarchy_series(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Splatoon 3 Anarchy Series information
        '''
        if (series_info := self.modes[node].anarchy_series) is None:
            return None

        file = await self.image_create(series_info, 'anarchy_series')
        time = await self.s3_rotation_update(series_info)

        anarchy_series = discord.Embed(color=discord.Color.orange())
        anarchy_series.add_field(name=f'Anarchy Series - {series_info.gamemode}', value=time)
        anarchy_series.set_image(url='attachment://anarchy_series.png')
        anarchy_series.set_footer(text=f'{series_info.maps[0].name} | {series_info.maps[1].name}')

        return [anarchy_series, file]


    async def anarchy_open(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Splatoon 3 Anarchy Open information
        '''
        if (open_info := self.modes[node].anarchy_open) is None:
            return None

        file = await self.image_create(open_info, 'anarchy_open')
        time = await self.s3_rotation_update(open_info)

        anarchy_open = discord.Embed(color=discord.Color.dark_orange())
        anarchy_open.add_field(name=f'Anarchy Open - {open_info.gamemode}', value=time)
        anarchy_open.set_image(url='attachment://anarchy_open.png')
        anarchy_open.set_footer(text=f'{open_info.maps[0].name} | {open_info.maps[1].name}')

        return [anarchy_open, file]


    async def x_battles(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Splatoon 3 X Battle information
        '''
        if (x_info := self.modes[node].x_battles) is None:
            return None

        elif x_info.fest_active is True:
            return None

        file = await self.image_create(x_info, 'x_battles')
        time = await self.s3_rotation_update(x_info)
        
        x_battles = discord.Embed(color=discord.Color.dark_green())
        x_battles.add_field(name=f'X Battle - {x_info.gamemode}', value=time)
        x_battles.set_image(url='attachment://x_battles.png')
        x_battles.set_footer(text=f'{x_info.maps[0].name} | {x_info.maps[1].name}')

        return [x_battles, file]


    async def challenges(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Challenge information
        '''

        if (challenges := self.modes[node].challenge) is None:
            return None

        file = await self.image_create(challenges, 'challenges')

        challenge = discord.Embed(title=f'Challenge: {challenges.title}', description=challenges.description, color=discord.Color.from_rgb(244, 79, 148))
        challenge.add_field(name=f"{challenges.gamemode} - {challenges.maps[0].name} | {challenges.maps[1].name}", value=challenges.extended_description, inline=False)
        timeslot = f''


        for i in range(len(challenges.times)):
            timeslot += f'Starts <t:{challenges.times[i].start}:F> <t:{challenges.times[i].start}:R>\nEnds <t:{challenges.times[i].end}:F> <t:{challenges.times[i].end}:R>\n\n'

        challenge.add_field(name='Time Slots For This Challenge', value=timeslot, inline=False)
        challenge.set_image(url='attachment://challenges.png')
        challenge.set_footer(text=f'{challenges.maps[0].name} | {challenges.maps[1].name}')

        return [challenge, file]


    async def salmon_run(self, node: int) -> discord.Embed | None:
        '''
        Returns Salmon Run information in an embed
        '''

        if (salmon_info := self.modes[node].salmon_run) is None:
            return None

        salmon_run = discord.Embed(title='Salmon Run', description=f'Start time: <t:{salmon_info.times.start}:f>, <t:{salmon_info.times.start}:R>\nEnd Time: <t:{salmon_info.times.end}:f>, <t:{salmon_info.times.end}:R>', color=discord.Color.purple())
        salmon_run.add_field(name=f"{salmon_info.stage.name} - {salmon_info.boss}", value='\n'.join(weapon for weapon in salmon_info.weapons))
        salmon_run.set_image(url=salmon_info.stage.image)
        salmon_run.set_thumbnail(url='https://cdn.wikimg.net/en/splatoonwiki/images/6/66/S3_Badge_Grizzco_10K.png')
        salmon_run.set_footer(text='Powered by **Splatoon3.ink**')

        return salmon_run


    async def big_run(self) -> discord.Embed | None:
        '''
        Returns Big Run information
        '''

        if (big_run_info := self.modes[0].big_run) is None:
            return None

        big_run = discord.Embed(title='Big Run', description=f'Start time: <t:{big_run_info.time.start}:f>, <t:{big_run_info.time.start}:R>\nEnd Time: <t:{big_run_info.time.end}:f>, <t:{big_run_info.time.end}:R>', color=discord.Color.purple())
        big_run.add_field(name=f"{big_run_info.stage.name} - {big_run_info.boss}",value='\n'.join(weapon for weapon in big_run_info.weapons))
        big_run.set_image(url=big_run_info.stage.image)
        big_run.set_thumbnail(url='https://cdn.wikimg.net/en/splatoonwiki/images/thumb/9/98/S3_Icon_Big_Run.svg/1200px-S3_Icon_Big_Run.svg.png')
        big_run.set_footer(text='Powered by **Splatoon3.ink**')

        return big_run


    async def eggstra_work(self) -> discord.Embed | None:
        '''
        Returns Eggstra Work information when available
        '''
        if (eggstra_work_info := self.modes[0].eggstra_work) is None:
            return None

        eggstra_work = discord.Embed(title='EGGSTRA WORK', description=f'Start time: <t:{eggstra_work_info.time.start}:f>, <t:{eggstra_work_info.time.start}:R>\nEnd Time: <t:{eggstra_work_info.time.end}:f>, <t:{eggstra_work_info.time.end}:R>', color=discord.Color.gold())
        eggstra_work.add_field(name=f"{eggstra_work_info.stage.name}", value='\n'.join(weapon for weapon in eggstra_work_info.weapons))
        eggstra_work.set_image(url=eggstra_work_info.stage.image)
        eggstra_work.set_thumbnail(url='https://cdn.wikimg.net/en/splatoonwiki/images/thumb/7/77/S3_Icon_Eggstra_Work.svg/120px-S3_Icon_Eggstra_Work.svg.png?20230220215341')
        eggstra_work.set_footer(text='Enjoy the event!')

        return eggstra_work


    async def splatfest_open(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Splatfest Open information in an embed when a Splatfest is active
        '''
        splatfest_info = self.modes[node].splatfest_open

        if splatfest_info is None or splatfest_info.fest_active is False:
            return None

        file = await self.image_create(splatfest_info, 'splatfest_open')
        time = await self.s3_rotation_update(splatfest_info)

        splatfest_open = discord.Embed(title=f'Splatfest Battle - {splatfest_info.mode}', description=time, color=discord.Color.dark_blue())
        splatfest_open.set_image(url='attachment://splatfest_open.png')
        splatfest_open.set_footer(text=f'{splatfest_info.maps[0].name} | {splatfest_info.maps[1].name}')

        return [splatfest_open, file]


    async def splatfest_pro(self, node: int) -> list[discord.Embed | discord.File] | None:
        '''
        Returns Splatfest information in an embed when a Splatfest is active
        '''
        splatfest_info = self.modes[node].splatfest_pro

        if splatfest_info is None or splatfest_info.fest_active is False:
            return None

        file = await self.image_create(splatfest_info, 'splatfest_pro')
        time = await self.s3_rotation_update(splatfest_info)

        splatfest_pro = discord.Embed(title=f'Splatfest Battle - {splatfest_info.mode}', description=time, color=discord.Color.dark_blue())
        splatfest_pro.set_image(url='attachment://splatfest_pro.png')
        splatfest_pro.set_footer(text='attachment://splatfest_pro.png')

        return [splatfest_pro, file]
    
    async def tricolor_battle(self) -> discord.Embed | None:
        tricolor_info = self.modes[0].tricolor_battle
        if tricolor_info is None or tricolor_info.is_available is False:
            return None
        
        tricolor_stage = discord.Embed(title=f'Tricolor Battle', description=f'Start time: <t:{tricolor_info.availability.start}:f>, <t:{tricolor_info.availability.start}:R>\nEnd Time: <t:{tricolor_info.availability.end}:f>, <t:{tricolor_info.availability.end}:R>')
        tricolor_stage.set_image(url=tricolor_info.stage.image)
        tricolor_stage.set_footer(text=tricolor_info.stage.name)

        return tricolor_stage


    @app_commands.command(name='s3_maps', description='Displays the current rotations for Splatoon 3')
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = None):
        mode = mode.title().strip()

        match mode:
            case None:
                current = ModeEmbeds(
                    turf_war=await self.turf_war(0),
                    anarchy_series=await self.anarchy_series(0),
                    anarchy_open=await self.anarchy_open(0),
                    x_battle=await self.x_battles(0),
                    salmon_run=await self.salmon_run(0),
                    challenge=await self.challenges(0),
                    big_run=await self.big_run(),
                    eggstra_work=await self.eggstra_work(),
                    splatfest_open=await self.splatfest_open(0),
                    splatfest_pro=await self.splatfest_pro(0),
                    tricolor_battle=await self.tricolor_battle()
                )

                current_info = [mode for modes in [current.splatfest_open, current.splatfest_pro, current.turf_war, current.anarchy_series, current.anarchy_open, current.x_battle, current.challenge] if modes is not None for mode in modes]
                current_info.extend([mode for mode in [current.salmon_run, current.big_run, current.eggstra_work, current.tricolor_battle] if mode is not None])

                modes = [embed for embed in current if type(embed) is discord.Embed]
                files = [image for image in current if type(image) is discord.File]

                await interaction.response.send_message(embeds=modes, files=files)

            case 'Turf War':
                turf_war = await self.turf_war(0)
                await interaction.response.send_message(embed=turf_war[0], file=turf_war[1])

            case 'Anarchy Series':
                anarchy_series = await self.anarchy_series(0)
                await interaction.response.send_message(embed=anarchy_series[0], file=anarchy_series[1])

            case 'Anarchy Open':
                anarchy_open = await self.anarchy_open(0)
                await interaction.response.send_message(embed=anarchy_open[0], file=[1])

            case 'X Battles':
                x_battles = await self.x_battles(0)
                await interaction.response.send_message(embed=x_battles[0], file=x_battles[1])

            case 'Challenge':
                challenge = await self.challenges(0)
                if challenge:
                    await interaction.response.send_message(embed=challenge[0], file=challenge[1])

                else:
                    await interaction.response.send_message(content='There aren\'t any challenges on the horizon', ephemeral=True)

            case 'Salmon Run':
                salmon_run = await self.salmon_run(0)
                await interaction.response.send_message(embed=salmon_run)

            case 'Eggstra Work':
                eggstra_work = await self.eggstra_work()
                if eggstra_work:
                    await interaction.response.send_message(embed=eggstra_work)

                else:
                    await interaction.response.send_message(content='No Eggstra Work soon', ephemeral=True)

            case 'Big Run':
                big_run = await self.big_run()
                if big_run:
                    await interaction.response.send_message(embed=big_run)

                else:
                    await interaction.response.send_message(content='No Big Run soon', ephemeral=True)

            case 'Splatfest Open':
                splatfest_open = await self.splatfest_open(0)
                if splatfest_open[0]:
                    await interaction.response.send_message(embed=splatfest_open[0], file=splatfest_open[1])

                else:
                    await interaction.response.send_message(content='Not currently a Splatfest', ephemeral=True)

            case 'Splatfest Pro':
                splatfest_pro = await self.splatfest_open(0)
                if splatfest_pro[0]:
                    await interaction.response.send_message(embed=splatfest_pro[0], file=splatfest_pro[1])

                else:
                    await interaction.response.send_message(content='Not currently a Splatfest', ephemeral=True)
            
            case 'Tricolor Battle':
                tricolor = self.tricolor_battle()
                if tricolor:
                    await interaction.response.send_message(embed=tricolor)
                
                else:
                    await interaction.response.send_message(content='Tricolor Battles not currently unlocked', ephemeral=True)

            case _:
                await interaction.response.send_message(content='That is not a valid game mode', ephemeral=True)


    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'X Battles', 'Challenge', 'Salmon Run', 'Eggstra Work', 'Big Run', 'Splatfest Open', 'Splatfest Pro', 'Tricolor Battle']
        return [app_commands.Choice(name=mode, value=mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel: discord.TextChannel) -> None:
        await channel.purge()
        await asyncio.sleep(1)

        current = ModeEmbeds(
            turf_war=await self.turf_war(0),
            anarchy_series=await self.anarchy_series(0),
            anarchy_open=await self.anarchy_open(0),
            x_battle=await self.x_battles(0),
            salmon_run=await self.salmon_run(0),
            challenge=await self.challenges(0),
            big_run=await self.big_run(),
            eggstra_work=await self.eggstra_work(),
            splatfest_open=await self.splatfest_open(0),
            splatfest_pro=await self.splatfest_pro(0),
            tricolor_battle=await self.tricolor_battle()
        )

        future = ModeEmbeds(
            turf_war=await self.turf_war(1),
            anarchy_series=await self.anarchy_series(1),
            anarchy_open=await self.anarchy_open(1),
            x_battle=await self.x_battles(1),
            salmon_run=await self.salmon_run(1),
            challenge=await self.challenges(1),
            big_run=await self.big_run(),
            eggstra_work=await self.eggstra_work(),
            splatfest_open=await self.splatfest_open(1),
            splatfest_pro=await self.splatfest_pro(1),
            tricolor_battle=await self.tricolor_battle()
        )

        current_modes = [mode for modes in [current.splatfest_open, current.splatfest_pro, current.turf_war, current.anarchy_series, current.anarchy_open, current.x_battle, current.challenge] if modes is not None for mode in modes]
        current_modes.append(current.salmon_run)

        future_modes = [mode for modes in [future.splatfest_open, future.splatfest_pro, future.turf_war, future.anarchy_series, future.anarchy_open, future.x_battle, future.challenge] if modes is not None for mode in modes]
        extra_future = [mode for mode in [future.salmon_run, current.big_run, current.eggstra_work] if mode is not None]
        future_modes.extend(extra_future)

        gamemodes = [embed for embed in current_modes if type(embed) is discord.Embed]
        gamemode_files = [image for image in current_modes if type(image) is discord.File]

        future_gamemodes = [embed for embed in future_modes if type(embed) is discord.Embed]
        future_gamemode_files = [image for image in future_modes if type(image) is discord.File]

        await channel.send(embeds=gamemodes, files=gamemode_files)
        await channel.send(content='------------------------------------------------')
        await channel.send(embeds=future_gamemodes, files=future_gamemode_files)


    @app_commands.command(name='schedule_task', description='Use this command to start the task in the used channel')
    async def schedule_task(self, interaction: discord.Interaction) -> None:
        guild_id = str(interaction.guild_id)
        
        if await self.bot.is_owner(interaction.user) is False:
            await interaction.response.send_message('You need to be the bot owner to use this!', ephemeral=True)
            return
        

        with open('servers.json', 'r+') as file:
            js: dict = json.load(file)

            if guild_id in js.keys():
                if interaction.channel.name in js[guild_id]['Channels']:
                    await interaction.response.send_message('Splatoon 3 rotations are already being displayed here', ephemeral=True)
                    return
                
                else:
                    js[guild_id]['Guild Name'] = interaction.guild.name
                    js[guild_id]['Channels'][interaction.channel.name] = interaction.channel_id
            
            else:
                js[guild_id] = {'Guild Name': interaction.guild.name, 'Channels': {interaction.channel.name: interaction.channel_id}}

            file.seek(0)
            json.dump(js, file, indent=4)

        await interaction.response.send_message('Splatoon 3 rotations should be updating here', ephemeral=True)
                
                
    @tasks.loop(seconds=10.0)
    async def embed_send(self) -> None:
        await self.api_call()

        with open('servers.json', 'r') as file:
            js: dict = json.load(file)

        for guild in js:
            for channel in js[guild]['Channels']:
                channel = await self.bot.fetch_channel(js[guild]['Channels'][channel])
                await self.channel_setup(channel)

        self.embed_send.change_interval(time=time_calc())


    @embed_send.before_loop
    async def before_embed_send_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(maps_modes(bot))
