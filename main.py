import discord
from discord.ext import commands
from tokey import token
from Responses import responses
import os

OP = "!"
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    commands = responses.keys()
    if message.content.startswith(OP):
        if message.content[1:] in commands:
            await message.channel.send(responses[message.content[1:]])

client.run(token())

if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
