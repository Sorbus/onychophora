import discord
import asyncio
from helpers import Config

client = discord.Client()
config = Config()

@client.event
async def on_ready():
    """
    report on startup
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # server = None
    # for s in client.servers:
    #     if int(s.id) == 239675999959121921:
    #         server = s
    #         break

    # member = None
    # for m in server.members:
    #     if int(m.id) == 163476908493766656:
    #         member = m
    #         break

    # role = None
    # for r in server.role_hierarchy:
    #     if r.name == "mods":
    #         role = r
    #         break

    # await client.add_roles(member, role)
    # await client.logout()

@client.event
async def on_message(message):
    if int(message.author.id) == 163476908493766656:
        print(message.content)
        if "please kick me" in message.content:
            await client.kick(message.author)
            await client.send_message(message.channel, "{} has been removed from the server.".format(message.author.name))

@client.event
async def on_member_join(member):
    """
    restore moderator privileges when I rejoin the speakeasy
    """
    if (int(member.id) == 163476908493766656 and
            int(member.server.id) == 239675999959121921):
        role = None
        for potential_role in member.server.role_hierarchy:
            if potential_role.name == "mods":
                role = potential_role
                break
        await client.add_roles(member, role)
        await client.logout()

client.run(config.tokens['barmaid'])
