import discord, os, tokey
import youtubeHandler_v2 as yh
from discord.ext import commands

import youtubeHandler_v2 as yh


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


dl = yh.music_downloader()

u = "https://www.youtube.com/watch?v=elQGj6uar1A"
url = "https://www.youtube.com/playlist?list=PL_gcregDRpNvowOVYzKQHJYcKX6setQAY"


shit = dl.get_info("https://www.youtube.com/watch?v=Vqbk9cDX0l0&t=6s")
print(shit)




#string = "shit ** \\ fuck"
#for x in dl.fix_title(string):
#    shit = string.split(string[x.span()[0]:x.span()[1]])
#    print(shit[0], '\n', shit[1])
#    #print(string[x.span()[0]:x.span()[1]])
#    string.replace(string[x.span()[0]:x.span()[1]], "_")
#print(dl.fix_title(string))
#print(shit)
#for x in shit:
#    path = "songs/" + x[0] + ".mp3"
#    print(path)
#    if os.path.isfile(path): print("shit")
#    else:print('no')
#

#shit2 = dl.get_info(u)
#client.run(tokey.token())

#webpage_url is the one to get url for vid from playlist entries