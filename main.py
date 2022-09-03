import discord, os, tokey
from discord.ext import commands
import youtubeHandler as yh


PREFIX = "!"
client = commands.Bot(command_prefix=PREFIX)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

#dl = yh.music_downloader()
#url = "https://www.youtube.com/playlist?list=PL_gcregDRpNt2tOoG4bgaTIUeozdXfBT_"
#shit = dl.get_info("https://www.youtube.com/playlist?list=PL_gcregDRpNvYOVyLQ9i9tfuNDatXj4w4")
#print(shit)



client.run(tokey.token())

#webpage_url is the one to get url for vid from playlist entries