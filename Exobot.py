import discord, asyncio, random
from discord.ext import commands
from tokey import token
import youtubeHandler

PREFIX = "!"
client = commands.Bot(command_prefix=PREFIX)
queue = []
#   have bot auto disconect after not playing anything for a set amount of time

def get_vc(ctx):
    """
    connects to vc
    :param author: command author
    :return: None
    """
    for chan in ctx.guild.voice_channels:
        if ctx.author.id in chan.voice_states.keys():
            return chan
    return None

def get_voice(ctx):
    return discord.utils.get(client.voice_clients, guild=ctx.guild)

async def con(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=get_vc(ctx).name)
    if voiceChannel:
        try:
            await voiceChannel.connect()
        except Exception as e:
            print(e)

async def song_geter(url):
    dl = youtubeHandler.music_downloader()
    song = dl.get_song(url)
    return song

def add_queue(song):
    queue.append(song)


@client.command()
async def play(ctx, url : str):
    """
    find correct vc
    connect to vc
    add song to que
    start playing from que
    after song plays remove from que
    play next song in que
        if not other song is in que
            wait for a bit and disconnect if nothing else added
    """
    await ctx.send("whatever fuck you I'm doing it")

    sg = asyncio.create_task(song_geter(url))

    try:
        voice = get_voice(ctx)
        if not voice:
            await con(ctx)
        voice = get_voice(ctx)

        if voice.channel != get_vc(ctx):
            await voice.disconnect()
            await con(ctx)
            voice = get_voice(ctx)
    except:
        await ctx.send("you rat bastard. You aren't even in here!")
        return
    #need to make reconnect for songs that take long to downloadn

    await sg
    song = sg.result()
    if type(song) == list:
        if len(song) > 0:
            for x in song: queue.append(x)
            song = queue.pop(0)
        else: print('empty list')
    def after_play(err):
        if len(queue) > 0:
            next_song = queue.pop(0)
            voice.play(discord.FFmpegPCMAudio(next_song), after=after_play)

    try:
        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(song), after=after_play)
        elif voice.is_playing():
            add_queue(song)
    except Exception as e: print(e)
@client.command()
async def shuffle(ctx):
    global queue
    queue = random.shuffle(queue)

@client.command()
async def loop(ctx):
    pass

@client.command()
async def connect(ctx):
    voice = get_voice(ctx)
    if not voice:
        await con(ctx)
    voice = get_voice(ctx)

    if voice.channel != get_vc(ctx):
        await voice.disconnect()
        await con(ctx)
        voice = get_voice(ctx)

@client.command()
async def stop(ctx):
    global queue
    queue = []
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def skip(ctx):
    voice = get_voice(ctx)

    voice.stop()

@client.command()
async def leave(ctx):
    voice = get_voice(ctx)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I'm already gone, can you leave?")

@client.command()
async def pause(ctx):
    voice = get_voice(ctx)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("can't stop wwhat I'm not doing")

@client.command()
async def resume(ctx):
    voice = get_voice(ctx)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("I'm already runnin")

client.run(token())
