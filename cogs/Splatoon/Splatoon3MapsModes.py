from models import ScheduleResponse, ProcessedReturns
from utils.sessions import fetch_data, get_session
from models.SplatoonModels import PvP, PvE
from discord.ext import commands, tasks
from discord import app_commands
from datetime import timedelta
from io import BytesIO
from PIL import Image
import asyncio
import discord
import json


class maps_modes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.response = None
        self.session = None
        self.embed_send.start()

    async def image_create[T: PvP](self, mode: type[T], filename: str) -> discord.File:
        '''
        Creates Discord File objects to use in other functions
        '''
        imgs = []
        for map in range(2):
            async with self.session.get(mode.maps[map].image_url.encoded_string()) as response:
                imgs.append(await response.read())

        stage_one = Image.open(BytesIO(imgs[0]))
        stage_two = Image.open(BytesIO(imgs[1]))
        
        merged = Image.new('RGB', (stage_one.width + stage_two.width, stage_one.height))
        merged.paste(stage_one, (0, 0))
        merged.paste(stage_two, (stage_one.width, 0))

        final = BytesIO()
        merged.save(final, format='PNG')
        final.seek(0)

        return discord.File(fp=final, filename=f'{filename}.png')

    async def s3_rotation_update[T: (PvP, PvE)](self, mode: type[T]) -> str:
        '''
        Returns a string embedded with Unix timestamps formatted in a way Discord displays local time
        '''
        start = int(mode.start.timestamp())
        end = int(mode.end.timestamp())
        return f'Start Time: <t:{start}:t>, <t:{start}:R>\nEnd Time: <t:{end}:t>, <t:{end}:R>'

    async def pve_modes[T: PvE](self, title: str, mode: type[T], color: discord.Color) -> ProcessedReturns | None:
        if mode is None:
            return None

        if mode.boss is not None:
            stage = f'{mode.stage.name} - {mode.boss}'

        else:
            stage = mode.stage.name

        pve = discord.Embed(title=title, description=await self.s3_rotation_update(mode), color=color)
        pve.add_field(name=stage, value='\n'.join(weapon.weapon for weapon in mode.weapons))
        pve.set_image(url=mode.stage.image_url)
        pve.set_thumbnail(url=mode.mode_image)
        pve.set_footer(text='Powered by **Splatoon3.ink**')

        return ProcessedReturns(embed=pve)

    async def pvp_modes[T: PvP](self, mode: str, info: type[T], color: discord.Color) -> ProcessedReturns | None:
        '''
        Sets up the list containing the embed and file for some modes 
        '''
        if info is None or info.gamemode is None:
            return None

        readable_mode = mode.replace('_', ' ').title()

        # readable_mode puts "Battles" inside of itself depending on what gamem ode is being processed
        # This is done due to modes such as Anarchy Battles are split into multiple verisons while
        # Turf War and X Battles are just one game mode each
        if readable_mode not in ['Turf War', 'Tricolor', 'Splatfest Open', 'Splatfest Pro']:
            readable_mode = f'{readable_mode} - {info.gamemode}'

        file = await self.image_create(info, mode)
        time = await self.s3_rotation_update(info)

        embed = discord.Embed(color=color)
        embed.add_field(name=readable_mode, value=time)
        embed.set_image(url=f'attachment://{mode}.png')
        embed.set_footer(text=f'{info.maps[0].name} | {info.maps[1].name}')

        return ProcessedReturns(embed=embed, file=file)

    async def challenges(self, node: int) -> ProcessedReturns | None:
        '''
        Returns Challenge information
        '''
        if self.response.challenge is None:
            return None

        challenges = self.response.challenge[node]
        file = await self.image_create(challenges, 'challenges')

        challenge = discord.Embed(title=f'Challenge: {challenges.title}', description=challenges.description, color=discord.Color.from_rgb(244, 79, 148))
        challenge.add_field(name=f"{challenges.gamemode} - {challenges.maps[0].name} | {challenges.maps[1].name}", value=challenges.extended_description, inline=False)
        times = []

        for slot in range(len(challenges.time)):
            start = int(challenges.time[slot].start.timestamp())
            end = int(challenges.time[slot].end.timestamp())
            times.append(f'Starts <t:{start}:F> <t:{start}:R>\nEnds <t:{end}:F> <t:{end}:R>\n\n')

        timeslot = ''.join(times)
        challenge.add_field(name='Time Slots For This Challenge', value=timeslot, inline=False)
        challenge.set_image(url='attachment://challenges.png')
        challenge.set_footer(text=f'{challenges.maps[0].name} | {challenges.maps[1].name}')

        return ProcessedReturns(embed=challenge, file=file)

    async def tricolor_battle(self) -> ProcessedReturns | None:
        tricolor_info = self.response.tricolor_battles

        if tricolor_info is None:
            return None

        if tricolor_info.is_available is False:
            return None

        time = await self.s3_rotation_update(tricolor_info)

        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name='Tricolor Battle', value=time)
        embed.set_image(url=tricolor_info.maps[0].image_url)
        embed.set_footer(text=tricolor_info.maps[0].name)

        return ProcessedReturns(embed=embed)

    async def proper[T: (PvP, PvE)](self, data: type[T], index: int) -> type[T] | None: # function name wayyyy too vague
        return data[index] if index < len(data) else None

    async def prep_embeds(self, node: int) -> dict[str, ProcessedReturns | None]:
        modes = {
            'Turf War': await self.pvp_modes(mode='turf_war', info=await self.proper(data=self.response.turf_war, index=node), color=discord.Colour.green()),
            'Anarchy Series': await self.pvp_modes(mode='anarchy_series', info=await self.proper(data=self.response.anarchy_series, index=node), color=discord.Colour.orange()),
            'Anarchy Open': await self.pvp_modes(mode='anarchy_open', info=await self.proper(data=self.response.anarchy_open, index=node), color=discord.Colour.dark_orange()),
            'X Battles': await self.pvp_modes(mode='x_battles', info=await self.proper(data=self.response.x_battles, index=node), color=discord.Colour.dark_green()),
            'Challenge': await self.challenges(node),
            'Splatfest Open': await self.pvp_modes(mode='splatfest_open', info=await self.proper(data=self.response.splatfest_open, index=node), color=discord.Colour.dark_blue()),
            'Splatfest Pro': await self.pvp_modes(mode='splatfest_pro', info=await self.proper(data=self.response.splatfest_pro, index=node), color=discord.Colour.dark_blue()),
            'Tricolor Battle': await self.tricolor_battle(),
            'Salmon Run': await self.pve_modes(title='Salmon Run', mode=await self.proper(data=self.response.salmon_run, index=node), color=discord.Colour.purple()),
            'Big Run': await self.pve_modes(title='Big Run', mode=await self.proper(data=self.response.big_run, index=0), color=discord.Colour.purple()),
            'Eggstra Work': await self.pve_modes(title='Eggstra Work', mode=await self.proper(data=self.response.eggstra_work, index=node), color=discord.Colour.gold())
        }

        filtered = {k: v for k, v in modes.items() if v is not None}
        return filtered

    @app_commands.command(name='s3_maps', description='Displays the current rotations for Splatoon 3')
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def s3_maps_modes(self, interaction: discord.Interaction, mode: str = None):
        await interaction.response.defer(thinking=True)
        if mode:
            mode = mode.title().strip()

        current = await self.prep_embeds(node=0)

        if mode is None:
            current_info = list(current.values())
            modes = list(filter(None, [value.embed for value in current_info]))
            files = list(filter(None, [value.file for value in current_info]))
    
            await interaction.followup.send(embeds=modes, files=files)
            return

        elif mode not in current.keys():
            await interaction.followup.send(content='Mode unavailable or invalid', ephemeral=True)
            return

        if current[mode].file is not None:
            await interaction.followup.send(embed=current[mode].embed, file=current[mode].file)
            return

        await interaction.followup.send(embed=current[mode].embed)

    @s3_maps_modes.autocomplete('mode')
    async def s3_maps_modes_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        modes = ['Turf War', 'Anarchy Series', 'Anarchy Open', 'X Battles', 'Challenge', 'Salmon Run', 'Eggstra Work', 'Big Run', 'Splatfest Open', 'Splatfest Pro', 'Tricolor Battle']
        return [app_commands.Choice(name=mode, value=mode) for mode in modes if current.lower() in mode.lower()]

    async def channel_setup(self, channel: discord.TextChannel) -> None:
        await channel.purge()
        await asyncio.sleep(1)

        current = await self.prep_embeds(node=0)
        future = await self.prep_embeds(node=1)

        current = list(current.values())
        future = list(future.values())

        gamemodes = list(filter(None, [value.embed for value in current]))
        gamemode_files = list(filter(None, [value.file for value in current]))

        future_gamemodes = list(filter(None, [value.embed for value in future]))
        future_gamemode_files = list(filter(None, [value.file for value in future]))

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

    @tasks.loop(seconds=20.0)
    async def embed_send(self) -> None:
        self.response = await fetch_data(url='https://splatoon3.ink/data/schedules.json', model=ScheduleResponse)

        with open('servers.json', 'r') as file:
            js: dict = json.load(file)

        for guild in js:
            for channel in js[guild]['Channels']:
                channel = await self.bot.fetch_channel(js[guild]['Channels'][channel])
                await self.channel_setup(channel)

        start = self.response.turf_war[0].end
        start_time = start if start else self.response.splatfest_open[0].end
        start_time += timedelta(minutes=1)

        self.embed_send.change_interval(time=start_time.timetz())

    @embed_send.before_loop
    async def before_embed_send_loop(self):
        await self.bot.wait_until_ready()
        self.session = await get_session()

async def setup(bot: commands.Bot):
    await bot.add_cog(maps_modes(bot))
