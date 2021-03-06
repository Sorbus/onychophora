import discord
import asyncio
import re
import random
from helpers import Config

client = discord.Client()
config = Config()

channels = {}

owners = [111272999478394880, 163476908493766656]

pattern = re.compile(r'^\.send ([\-\w]+) ([^$]+)$', flags=re.IGNORECASE)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for server in client.servers:
        if int(server.id) == 239675999959121921:
            for channel in server.channels:
                # print("storing {}".format(channel.name))
                channels[channel.name] = channel

@client.event
async def on_message(message: discord.Message):
    if message.channel.is_private and int(message.author.id) in owners:
        match = re.fullmatch(pattern, message.content)

        if match: 
            if match.group(1) in channels:
                await client.send_typing(channels[match.group(1)])
                await asyncio.sleep(random.randint(1, 5), loop=client.loop)
                await client.send_message(channels[match.group(1)], match.group(2))
            else:
                print("channel not found")
        else:
            #print("no match")
            pass
    else:
        #print("invalid channel or user")
        pass

client.run(config.tokens['barmaid'])
