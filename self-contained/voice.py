import discord
import asyncio
# from gmusicapi import Mobileclient
from helpers import Config

client = discord.Client()
# api = Mobileclient()
config = Config()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message: discord.Message):
    if message.author.name == "Else":
        if message.content == "tock":
            channel = message.author.voice_channel
            if channel:
                print(message.author.name + " in " + channel.id + " [" + channel.name + "]")
                voice = await client.join_voice_channel(channel)
                player = voice.create_ffmpeg_player('tick.mp3', options="-application lowdelay -packet_loss 10 -ar 32000")
                player.volume = 0.7
                player.start()
            else:
                print("not in voice")
        else:
            print(message.content)

client.run(config.tokens['barmaid'])