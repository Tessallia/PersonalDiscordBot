import discord, asyncio, random, os
from discord.ext import commands
from logs.log import *
import youtubeHandler_v2 as yh

class Exobot(commands.Cog):
#    PREFIX = "!"
#    client = commands.Bot(command_prefix=PREFIX)

    def __init__(self, client):

        self.client = client

        self.exo_log = create_logger(__name__, logging.ERROR, './logs')
        self.queue = []
        self.loop = False
        self.voice = None



    def get_vc(self,ctx):
        for chan in ctx.guild.voice_channels:
            if ctx.author.id in chan.voice_states.keys():
                return chan
        return None

    def get_voice(self, ctx): self.voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    async def get_voicechannel(self, ctx):
        name = self.get_vc(ctx).name
        if name:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=name)
        elif not name:
            await ctx.send('get in vc first loser')

        try: await voiceChannel.connect()
        except Exception as e: self.exo_log.error(e)

    def correctvc(self, ctx):
        if self.voice.channel == self.get_vc(ctx): return True
        else: return False

    async def movevc(self, ctx):
        await self.voice.disconnect()
        await self.get_voicechannel(ctx)
        self.get_voice(ctx)

    async def connect(self, ctx):
        try:
            await self.get_voicechannel(ctx)
            self.get_voice(ctx)
        except Exception as e: self.exo_log.error(e)

    async def song_dl(self, url):
        dl = yh.music_downloader()
        dl.download_url(url)
        return True

    async def song_paths(self, url):
        dl = yh.music_downloader()
        return dl.get_info(url)

    def after_play(self, err):
        if not self.loop: self.queue.pop(0)
        if len(self.queue) > 0:
            self.voice.play(discord.FFmpegPCMAudio('songs'+ os.sep + self.queue[0][0]+'.mp3'), after=self.after_play)

    @commands.command()
    async def play(self, ctx, url: str):
        await ctx.send("whatever fuck you I'm doing it")
        if not self.voice:
            await self.connect(ctx)
        if not self.correctvc(ctx):
            await self.movevc(ctx)

        #song download
        sdl = asyncio.create_task(self.song_dl(url))
        #song path list
        spl = asyncio.create_task(self.song_paths(url))

        await spl
        song = spl.result()
        try:
            if len(song) > 0:
                for x in song: self.queue.append(x)
            else: print('empty list')
        except Exception as e: self.exo_log.error(e+ "::song list::"+ song)
        try:
            self.voice.play(discord.FFmpegPCMAudio('songs'+ os.sep + self.queue[0][0]+'.mp3'), after=self.after_play)
        except Exception as e: print(e)
    @commands.command()
    async def skip(self, ctx):
        self.voice.stop()

    @commands.command()
    async def current(self, ctx):
        await ctx.send(self.queue[0][1])

    @commands.command()
    async def shuffle(self, ctx):
        random.shuffle(self.queue)
    @commands.command()
    async def loop(self,ctx):
        if self.loop: self.loop = False
        else: self.loop = True

    @commands.command()
    async def stop(self, ctx):
        self.queue = []
        self.voice.stop()

    @commands.command()
    async def leave(self, ctx):
        if self.voice.is_connected(): self.voice.disconnect()

    @commands.command()
    async def pause(self, ctx):
        if self.voice.is_playing(): self.voice.pause()

    async def resume(self, ctx):
        if self.voice.is_paused(): self.voice.resume()
def setup(client):
    client.add_cog(Exobot(client))