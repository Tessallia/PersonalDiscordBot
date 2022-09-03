import discord, asyncio, random, os
from discord.ext import commands
from logs.log import *
import youtubeHandler as yh

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
        else: self.queue.append(self.queue.pop(0))
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
        if not self.voice.is_connected():
            await self.connect(ctx)
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
    async def playlist1(self, ctx):
        #this just exist because the tyoutube downloader is constantly throttled so even downloading info is annoyingly long and
        #prevents bot from funcitoning
        await ctx.send("whatever fuck you I'm doing it")
        if not self.voice:
            await self.connect(ctx)
        if not self.correctvc(ctx):
            await self.movevc(ctx)
        self.queue =[["WEIRD MCDONALD'S RAP", 'https://www.youtube.com/watch?v=EtgNPaI8S60'], ['MC Virgins & Yung Nugget - Stay Strapped (Official Lyric Video)', 'https://www.youtube.com/watch?v=pe7RmhZgdOU'], ["Welcome to the Internet - Bo Burnham (from 'Inside' -- ALBUM OUT NOW)", 'https://www.youtube.com/watch?v=k1BneeJTDcU'], ['PINK GUY - HELP', 'https://www.youtube.com/watch?v=Ho1LgF8ys-c'], ["Friendship is Witchcraft- It'll be Ok", 'https://www.youtube.com/watch?v=uH2Ns9Tewpo'], ['All Eyes On Me', 'https://www.youtube.com/watch?v=tu5UjbEvyTA'], ['PINK GUY - STFU', 'https://www.youtube.com/watch?v=OLpeX4RRo28'], ['Bo Burnham - Bezos I (Audio)', 'https://www.youtube.com/watch?v=jHYRvIutN7s'], ['PINK GUY - KILL YOURSELF', 'https://www.youtube.com/watch?v=2dbR2JZmlWo'], ['Shit', 'https://www.youtube.com/watch?v=Nn8TL12lXR0'], ["Pinkie's brew lyrics", 'https://www.youtube.com/watch?v=R0Q7XlJERbA'], ['PINK GUY - FURR', 'https://www.youtube.com/watch?v=M34OyoBsXUk'], ['Pink Guy   Peanutbutter', 'https://www.youtube.com/watch?v=OS0EsoJ8LHk'], ['F_k Everything (Jon Lajoie)', 'https://www.youtube.com/watch?v=ulIOrQasR18'], ['Yung Nugget - The Imposter (Official Music Video)', 'https://www.youtube.com/watch?v=7Sp4ej6W2Q0'], ['Yung Nugget - Lightning Mcqueen', 'https://www.youtube.com/watch?v=wx3m7EM7pYs'], ['Yung Nugget - OnlyFans Girl (Official Lyric Video)', 'https://www.youtube.com/watch?v=uu0-HIMyfvc'], ["SANTA'S BROTHER - DICK PAYS RENT (FT. PINK GUY)", 'https://www.youtube.com/watch?v=E3FLI_XQonc'], ['PINK LIFE', 'https://www.youtube.com/watch?v=b9Wlei7ZV1Y'], ['pinkguy - animal man', 'https://www.youtube.com/watch?v=w38QD_1C8kY'], ['Erectile Dysfunction - Pink Guy (Pink Guy)', 'https://www.youtube.com/watch?v=9R_apkw4Xf0'], ["SANTA'S BROTHER - LADY'S MAN (GANGSTER RAP)", 'https://www.youtube.com/watch?v=_f4SXRMKzW8'], ["Yung Nugget - What's Your Kik_ (Official Lyric Video)", 'https://www.youtube.com/watch?v=wG3gJjVDfDQ'], ['FRIENDZONE SONG', 'https://www.youtube.com/watch?v=p37_Ux1G_BI'], ['JonTron & The Gregory Brothers - Being in Love Is Like Being on Drugs', 'https://www.youtube.com/watch?v=HHbkun8xCUc'], ['I Threw It On The Ground - LYRICS!!! (Lonley Island)', 'https://www.youtube.com/watch?v=l219P3Aws-Y'], ['Dick In A Box', 'https://www.youtube.com/watch?v=6e9iR-hNKWY'], ['SNL-Motherlover (Uncensored)', 'https://www.youtube.com/watch?v=r5wnIoMGzRc'], ['3-Way (The Golden Rule)', 'https://www.youtube.com/watch?v=_dLT15OF5hA'], ['BEST Zelda Rap EVER!! ANIMATED MUSIC VIDEO by Joel C - Starbomb', 'https://www.youtube.com/watch?v=0m9QUoW5KnY'], ['Bizarre- Justin Bieber ft. King Gordy', 'https://www.youtube.com/watch?v=fWLL6I7lpFI'], ["DVDA - Now You're a Man Lyrics", 'https://www.youtube.com/watch?v=851BqHMCaeM'], ['Circle Circle Dot Dot', 'https://www.youtube.com/watch?v=UjDQB-0_QKc'], ['Aqua - Barbie Girl (Audio)', 'https://www.youtube.com/watch?v=eLXXFVNFKww'], ['Wheeler Walker Jr. - Fuck You Bitch', 'https://www.youtube.com/watch?v=myJDBos5Vyw'], ['Tetris (Feat. London Yellow) (Prod. Maxokoolin)', 'https://www.youtube.com/watch?v=Cv0zTEDHPcQ'], ['pink  guy  - Nickelodeon Girls LYRIC', 'https://www.youtube.com/watch?v=ANbinXVa6WM'], ['Yung Nugget - Bruh Moment (8 PIECE MEAL OUT NOW)', 'https://www.youtube.com/watch?v=LjtWoDFTNO8'], ["Yung Nugget - Caught Lackin'", 'https://www.youtube.com/watch?v=bLnkIbNO-e0'], ["Luigi's Ballad - Starbomb (Lyrics) [HD]", 'https://www.youtube.com/watch?v=FQu4hxDhhTU'], ["STORY ANIMATIC - Star Bomb's 'Regretroid' (2014)", 'https://www.youtube.com/watch?v=7vIUsNXpS_A'], ["J Pee - I'm Not Gay (LYRIC VIDEO)", 'https://www.youtube.com/watch?v=uxLz5aWl4Mg'], ['Fried Noodles', 'https://www.youtube.com/watch?v=ZOLaYl3b-4w'], ['Das Racist - Combination Pizza Hut And Taco Bell', 'https://www.youtube.com/watch?v=EQ8ViYIeH04'], ['Rice Balls', 'https://www.youtube.com/watch?v=FhPPAJGQ_k8'], ['Scott Pilgrim vs. the World Ruined a Whole Generation of Women [Music Video]', 'https://www.youtube.com/watch?v=TSKizLRFbTo'], ['The Producers Hitler - Heil Myself', 'https://www.youtube.com/watch?v=yTBYksnK7N0'], ['Bo Burnham- Kill Yourself lyric video', 'https://www.youtube.com/watch?v=w3nFWbRSYn8'], ['Bo Burnham - Lower Your Expectations _ Lyrics_Letra _ Subtitulado al Español', 'https://www.youtube.com/watch?v=FA9N_YKWmag'], ['Master Chief vs Leonidas. Epic Rap Battles of History', 'https://www.youtube.com/watch?v=mgVwv0ZuPhM'], ['Mr T vs Mr Rogers. Epic Rap Battles of History', 'https://www.youtube.com/watch?v=7ZsKqbt3gQ0'], ['Christopher Columbus vs Captain Kirk. Epic Rap Battles of History', 'https://www.youtube.com/watch?v=xBzoBgfm55w'], ["'Weird Al' Yankovic - White & Nerdy (Official Music Video)", 'https://www.youtube.com/watch?v=N9qYF9DZPdw'], ['Weird Al Yankovic - Everything You Know Is Wrong', 'https://www.youtube.com/watch?v=KThlYHfIVa8'], ["'Weird' Al Yankovic - Amish Paradise (Official Parody of 'Gangsta's Paradise')", 'https://www.youtube.com/watch?v=lOfZLb33uCg'], ["Sub-Radio - Stacy's Dad (Full Video)", 'https://www.youtube.com/watch?v=WANlg297AHU'], ["I Don't Know What We're Talking About - NSP", 'https://www.youtube.com/watch?v=YhOadP3i3a8'], ["Welcome To My Parents' House - NSP", 'https://www.youtube.com/watch?v=3YXUWWZJXpE'], ["It's Bedtime - NSP", 'https://www.youtube.com/watch?v=MjPIbxFJdwg'], ['Thunder & Lightning - NSP', 'https://www.youtube.com/watch?v=-rSGoP5iGZQ'], ['Mansion Party - NSP', 'https://www.youtube.com/watch?v=dNoafUU4Ikw'], ['Release the Kraken - NSP', 'https://www.youtube.com/watch?v=4itm0SRxAro'], ['Heart Boner - NSP', 'https://www.youtube.com/watch?v=TS_OWTKCUIM'], ['Eating Food In The Shower - NSP', 'https://www.youtube.com/watch?v=zFyUn_4uL5E'], ['Samurai Abstinence Patrol - NSP', 'https://www.youtube.com/watch?v=yWXIZk2kTKQ'], ['Why I Cry - NSP', 'https://www.youtube.com/watch?v=lA__rwBKzSw'], ['Best Friends Forever!  -  NSP', 'https://www.youtube.com/watch?v=9uCft0PaGIM'], ['Attitude City - NSP', 'https://www.youtube.com/watch?v=bC3jD_l6q48'], ['Dinosaur Laser Fight  -  NSP', 'https://www.youtube.com/watch?v=LcmBALxDkRY'], ['The Decision  -  NSP', 'https://www.youtube.com/watch?v=zUvH7cGiNl8'], ['No Reason Boner  -  NSP', 'https://www.youtube.com/watch?v=LOYQtbz_pPg'], ['Manticore  -  NSP', 'https://www.youtube.com/watch?v=rU8Wc6a1r7o'], ['FYI I Wanna F Your A  -  NSP', 'https://www.youtube.com/watch?v=LHIKf0f9E40'], ['Objects of Desire  -  NSP', 'https://www.youtube.com/watch?v=eu196vZSe_I'], ['Rhinoceratops vs. Superpuma  -  NSP', 'https://www.youtube.com/watch?v=JIRG8qELuXk'], ['Everybody Shut Up - NSP', 'https://www.youtube.com/watch?v=JEl96I_4PuI'], ['First Date - NSP', 'https://www.youtube.com/watch?v=UvgcLTzwjVM'], ['Dragon Slayer - NSP', 'https://www.youtube.com/watch?v=a5abgDBQHPk'], ['If We Were Gay  -  NSP', 'https://www.youtube.com/watch?v=f99njZJod2c'], ['Amazing Horse (Extended)', 'https://www.youtube.com/watch?v=VecVykoHCuU'], ["PINK GUY - SHE'S SO NICE", 'https://www.youtube.com/watch?v=5N_EBojQu5w'], ['Pink Guy   01 Ramen King', 'https://www.youtube.com/watch?v=D-YHWFTe72U'], ['Pink Guy   24 Loser', 'https://www.youtube.com/watch?v=fcVrgK3TM3Q'], ['Pink Guy   29 Took It In The Bottom', 'https://www.youtube.com/watch?v=idG0XF2DN7c'], ['Pink Guy   34 In Da Womb', 'https://www.youtube.com/watch?v=jEGBnslQpTU'], ['PINK GUY - DORA THE EXPLORA', 'https://www.youtube.com/watch?v=okQA7Bu2zm0'], ['PINK GUY - PLEASE STOP CALLING ME GAY', 'https://www.youtube.com/watch?v=4m-_kutqgDk'], ['PINK GUY - HOT NICKEL BALL ON A P_SSY', 'https://www.youtube.com/watch?v=LM6JaovnPsc']]
        try:
            self.voice.play(discord.FFmpegPCMAudio('songs' + os.sep + self.queue[0][0] + '.mp3'), after=self.after_play)
        except Exception as e:
            print(e)
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
