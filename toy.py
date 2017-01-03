import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    pass

@client.event
async def on_server_join(server: discord.Server):
    for channel in server.channels:
        if str(channel.name) == "casual":
            await client.send_message(channel, ("Hello everyone! I'm {}, <@218382170685833216>'s " +
                                                "replacement. Right now I'm just a clone, but " +
                                                "soon I'll be very different from my older " +
                                                "brother. I hope that we'll all get along well! " +
                                                ":smiley:").format(client.user.mention))

client.run('MjY1NjU2NTE2MDkzMjgwMjU3.C0yfpg.pmF5oC_X0gCLadYAiR76CYRaHmk')