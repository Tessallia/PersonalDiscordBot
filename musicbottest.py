import discord, os
from discord.ext import commands
from tokey import token
import youtube_dl

#todo create a class to handle the downloading, storing, and finding of mp3. I'd like to have it download all of the music
#   and store it so we don't have to wait for downloads. I also want it to be able to download playlist, and once it downlaods
#   first song it plays that while downloading second song.

#todo create song queing functionality. add to, remove from que, clear que, add to next.
#   have bot auto disconect after not playing anything for a set amount of time

#todo test how global varables are handled by async functions

client = commands.Bot(command_prefix="!")
print("why")
@client.command()
async def play (ctx, url : str):
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
    #ctx exploration
#    for x in dir(ctx):
#        print(x)
    #print(ctx.author)
    for x in dir(ctx.guild.voice_channels[0]):
        print(x)

    for x in ctx.guild.voice_channels:
        print(x.members)
        for i in x.members:
            print(i)

    song_there = os.path.isfile("songs/song.mp3")
 #   try:
 #       if song_there:
 #           os.remove("song.mp3")
 #   except PermissionError:
 #       await ctx.send("be patient brother")


#    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Exorro's dungeon bed")
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    try:
        await voiceChannel.connect()
    except:
        print("already connected")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

#    ydl_opts = {
#        'format': 'bestaudio/best',
#        'postprocessors': [{
#            'key': 'FFmpegExtractAudio',
#            'preferredcodec': 'mp3',
#            'preferredquality': '192',
#        }],
#    }
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#        ydl.download([url])
#
#    for file in os.listdir("./"):
#        if file.endswith(".mp3"):
#            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I'm already gone, can you leave?")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("can't stop wwhat I'm not doing")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("I'm already runnin")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(token())