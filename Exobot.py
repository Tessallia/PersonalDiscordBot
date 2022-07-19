import discord
from discord.ext import commands
from tokey import token
import youtube_dl

PREFIX = "!"
client = commands.Bot(command_prefix=PREFIX)
queue = []

def get_vc(ctx):
    """
    connects to vc
    :param author: command author
    :return: None
    """
    for chan in ctx.guild.voice_channels:
        if ctx.author.id in chan.voice_states.keys():
            return chan

def get_voice(ctx):
    return discord.utils.get(client.voice_clients, guild=ctx.guild)

async def con(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=get_vc(ctx).name)

    try:
        await voiceChannel.connect()
    except Exception as e:
        print(e)


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

    voice = get_voice(ctx)
    if not voice:
        await con(ctx)
    voice = get_voice(ctx)

    if voice.channel != get_vc(ctx):
        await voice.disconnect()
        await con(ctx)
        voice = get_voice(ctx)

    #get song



client.run(token())
