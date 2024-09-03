from .SplatoonUtils.GameModeClasses import ModeEmbeds
from .SplatoonUtils.ModesSetup import MapsModesSetup
from discord.ext import commands, tasks
from discord import app_commands
from zoneinfo import ZoneInfo
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

    async def api_call(self) -> None:
        '''
        Gathers the necessary information for the embeds
        '''

        modes = MapsModesSetup()
        await modes.gather([0, 1])
        self.modes = modes.gamemodes

    async def s3_rotation_update(self, node: int) -> discord.Embed:
        time = self.modes[node].turf_war
        rotation_update = discord.Embed(title='Splatoon 3 Rotations', description=f'Start Time: <t:{time.times.start}:t>, <t:{time.times.start}:R>\nEnd Time: <t:{time.times.end}:t>, <t:{time.times.end}:R>', color=discord.Color.blue())
        return rotation_update

    async def turf_war(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Turf War information
        '''

        turf_info = self.modes[node].turf_war

        if turf_info.fest_active is True:
            return None

        turf_war_stage_one = discord.Embed(color=discord.Color.green())
        turf_war_stage_one.add_field(name='Turf War', value='')
        turf_war_stage_one.set_image(url=turf_info.maps[0].image)
        turf_war_stage_one.set_footer(text=turf_info.maps[0].name)

        turf_war_stage_two = discord.Embed(color=discord.Color.green())
        turf_war_stage_two.set_image(url=turf_info.maps[1].image)
        turf_war_stage_two.set_footer(text=turf_info.maps[1].name)

        return turf_war_stage_one, turf_war_stage_two

    async def anarchy_series(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Series information
        '''
        if (series_info := self.modes[node].anarchy_series) is None:
            return None

        anarchy_series_one = discord.Embed(color=discord.Color.orange())
        anarchy_series_one.add_field(name=f'Anarchy Series - {series_info.gamemode}', value='')
        anarchy_series_one.set_image(url=series_info.maps[0].image)
        anarchy_series_one.set_footer(text=series_info.maps[0].name)

        anarchy_series_two = discord.Embed(color=discord.Color.orange())
        anarchy_series_two.set_image(url=series_info.maps[1].image)
        anarchy_series_two.set_footer(text=series_info.maps[1].name)

        return anarchy_series_one, anarchy_series_two

    async def anarchy_open(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 Anarchy Open information
        '''
        if (open_info := self.modes[node].anarchy_open) is None:
            return None

        anarchy_open_one = discord.Embed(color=discord.Color.dark_orange())
        anarchy_open_one.add_field(name=f'Anarchy Open - {open_info.gamemode}', value='')
        anarchy_open_one.set_image(url=open_info.maps[0].image)
        anarchy_open_one.set_footer(text=open_info.maps[0].name)

        anarchy_open_two = discord.Embed(color=discord.Color.dark_orange())
        anarchy_open_two.set_image(url=open_info.maps[1].image)
        anarchy_open_two.set_footer(text=open_info.maps[1].name)

        return anarchy_open_one, anarchy_open_two

    async def x_battles(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatoon 3 X Battle information
        '''
        if (x_info := self.modes[node].x_battles) is None:
            return None

        elif x_info.fest_active is True:
            return None

        x_one = discord.Embed(color=discord.Color.dark_green())
        x_one.add_field(name=f'X Battle - {x_info.gamemode}', value='')
        x_one.set_image(url=x_info.maps[0].image)
        x_one.set_footer(text=x_info.maps[0].name)

        x_two = discord.Embed(color=discord.Color.dark_green())
        x_two.set_image(url=x_info.maps[1].image)
        x_two.set_footer(text=x_info.maps[1].name)

        return x_one, x_two

    async def challenges(self, node: int) -> discord.Embed | None:
        '''
        Returns Challenge information
        '''

        if (challenges := self.modes[node].challenge) is None:
            return None

        challenge_one = discord.Embed(title=f'Challenge: {challenges.title}',
                                      description=challenges.description,
                                      color=discord.Color.from_rgb(244, 79, 148))

        challenge_one.add_field(name=f"{challenges.gamemode} - {challenges.maps[0].name} | {challenges.maps[1].name}", value=challenges.extended_description, inline=False)
        timeslot = f''
        for i in range(len(challenges.times)):
            timeslot += f'Starts <t:{challenges.times[i].start}:F> <t:{challenges.times[i].start}:R>\nEnds <t:{challenges.times[i].end}:F> <t:{challenges.times[i].end}:R>\n\n'

        challenge_one.add_field(name='Time Slots For This Challenge', value=timeslot, inline=False)

        challenge_one.set_image(url=challenges.maps[0].image)
        challenge_one.set_footer(text=challenges.maps[0].name)

        challenge_two = discord.Embed(color=discord.Color.from_rgb(244, 79, 148))
        challenge_two.set_image(url=challenges.maps[1].image)
        challenge_two.set_footer(text=challenges.maps[1].name)

        return challenge_one, challenge_two

    async def salmon_run(self, node: int) -> discord.Embed | None:
        '''
        Returns Salmon Run information in an embed
        '''

        if (salmon_info := self.modes[node].salmon_run) is None:
            return None

        salmon_run = discord.Embed(title='Salmon Run', description=f'Start time: <t:{salmon_info.times.start}:f>, <t:{salmon_info.times.start}:R>\nEnd Time: <t:{salmon_info.times.end}:f>, <t:{salmon_info.times.end}:R>', color=discord.Color.purple())
        salmon_run.add_field(name=f"{salmon_info.stage.name} - {salmon_info.boss}",
                             value='\n'.join(weapon for weapon in salmon_info.weapons))
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

    async def splatfest_open(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatfest Open information in an embed when a Splatfest is active
        '''
        splatfest_info = self.modes[node].splatfest_open

        if splatfest_info is None or splatfest_info.fest_active is False:
            return None

        splatfest_one = discord.Embed(title=f'Splatfest Battle - {splatfest_info.mode}', color=discord.Color.dark_blue())
        splatfest_one.set_image(url=splatfest_info.maps[0].image)
        splatfest_one.set_footer(text=splatfest_info.maps[0].name)

        splatfest_two = discord.Embed(color=discord.Color.dark_blue())
        splatfest_two.set_image(url=splatfest_info.maps[1].image)
        splatfest_two.set_footer(text=splatfest_info.maps[1].name)

        return splatfest_one, splatfest_two

    async def splatfest_pro(self, node: int) -> discord.Embed | None:
        '''
        Returns Splatfest information in an embed when a Splatfest is active
        '''
        splatfest_info = self.modes[node].splatfest_pro

        if splatfest_info is None or splatfest_info.fest_active is False:
            return None

        splatfest_one = discord.Embed(title=f'Splatfest Battle - {splatfest_info.mode}', color=discord.Color.dark_blue())
        splatfest_one.set_image(url=splatfest_info.maps[0].image)
        splatfest_one.set_footer(text=splatfest_info.maps[0].name)

        splatfest_two = discord.Embed(color=discord.Color.dark_blue())
        splatfest_two.set_image(url=splatfest_info.maps[1].image)
        splatfest_two.set_footer(text=splatfest_info.maps[1].name)

        return splatfest_one, splatfest_two
    
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
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = 'All'):
        mode = mode.title().strip()

        match mode:
            case 'All':
                rotation_update = await self.s3_rotation_update(0)
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

                current_modes = [mode for modes in [current.splatfest_open, current.splatfest_pro, current.turf_war,
                                                    current.anarchy_series, current.anarchy_open, current.x_battle, current.challenge] if modes is not None for mode in modes]
                await interaction.response.send_message(embeds=current_modes)

            case 'Turf War':
                rotation_update = await self.s3_rotation_update(0)
                turf_war_one, turf_war_two = await self.turf_war(0)
                await interaction.response.send_message(embeds=[rotation_update, turf_war_one, turf_war_two])

            case 'Anarchy Series':
                rotation_update = await self.s3_rotation_update(0)
                anarchy_series_one, anarchy_series_two = await self.anarchy_series(0)
                await interaction.response.send_message(embeds=[rotation_update, anarchy_series_one, anarchy_series_two])

            case 'Anarchy Open':
                rotation_update = await self.s3_rotation_update(0)
                anarchy_open_one, anarchy_open_two = await self.anarchy_open(0)
                await interaction.response.send_message(embeds=[rotation_update, anarchy_open_one, anarchy_open_two])

            case 'X Battles':
                rotation_update = await self.s3_rotation_update(0)
                x_one, x_two = await self.x_battles(0)
                await interaction.response.send_message(embeds=[rotation_update, x_one, x_two])

            case 'Challenge':
                challenge_one, challenge_two = await self.challenges(0)
                if challenge_one:
                    await interaction.response.send_message(embeds=[challenge_one, challenge_two])

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

            case _:
                await interaction.response.send_message(content='That is not a valid game mode', ephemeral=True)

    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'X Battles', 'Challenge', 'Salmon Run', 'Eggstra Work', 'Big Run']
        return [app_commands.Choice(name=mode, value=mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel: discord.TextChannel) -> None:
        await channel.purge()
        await asyncio.sleep(1)

        rotation_update = await self.s3_rotation_update(0)
        future_rotation_update = await self.s3_rotation_update(1)

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

        current_modes = [mode for modes in [current.splatfest_open, current.splatfest_pro, current.turf_war,current.anarchy_series, current.anarchy_open, current.x_battle, current.challenge] if modes is not None for mode in modes]
        future_modes = [mode for modes in [future.splatfest_open, future.splatfest_pro, future.turf_war, future.anarchy_series, future.anarchy_open, future.x_battle, future.challenge] if modes is not None for mode in modes]

        gamemodes = list(filter(lambda mode: mode is not None, current_modes))
        salmon_run_stuff = list(filter(lambda mode: mode is not None, [current.salmon_run]))
        future_gamemodes = list(filter(lambda mode: mode is not None, future_modes))
        future_salmon_stuff = list(filter(lambda mode: mode is not None, [future.salmon_run, future.big_run, future.eggstra_work]))

        await channel.send(embed=rotation_update)
        await channel.send(embeds=gamemodes)
        await channel.send(embeds=salmon_run_stuff)

        await channel.send(content='------------------------------------------------')

        await channel.send(embed=future_rotation_update)
        await channel.send(embeds=future_gamemodes)
        await channel.send(embeds=future_salmon_stuff)


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
