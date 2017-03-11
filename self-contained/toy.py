import discord
import asyncio
import sys
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

    for item in client.servers:
        print('{}\t{}'.format(item.name, item.icon_url))

    # Demod Op

    # server = None
    # member = None
    # role = None

    # for item in client.servers:
    #     if int(item.id) is 239675999959121921:
    #         server = item
    #         break

    # for item in server.members:
    #     if int(item.id) is 194505708115329024:
    #         member = item
    #         break

    # for item in server.role_hierarchy:
    #     if item.name == "mods":
    #         role = item
    #         break

    # await client.remove_roles(member, role)

@client.event
async def on_message(message):
    print("{}\t{}\t{}".format(message.author.name, message.type, message.embeds))
    # if int(message.author.id) == 163476908493766656:
    #     print(message.content)
    #     if "please kick me" in message.content:
    #         await client.kick(message.author)
    #         await client.send_message(message.channel, "{} has been removed from the server.".format(message.author.name))
    # if int(message.author.id) == 84398290061250560:
    #     role = None
    #     for potential_role in message.server.role_hierarchy:
    #         if potential_role.name == "mods":
    #             role = potential_role
    #             break
    #     await client.add_roles(message.author, role)

@client.event
async def on_member_join(member):
    """
    restore privileges when I rejoin the speakeasy
    """
    if (int(member.id) == 163476908493766656 and
            int(member.server.id) == 239675999959121921):
        roles = []
        channel = None

        for potential_role in member.server.role_hierarchy:
            if potential_role.name in ['mods', 'code weaver', 'council']:
                roles.append(potential_role)

        for item in member.server.channels:
            if str(item.name) == 'judgement':
                channel = item

        if not channel:
            print("Could not find channel")
            return

        if len(roles) != 3:
            print("Could not find some roles")
            return

        await client.add_roles(member, roles[0], roles[1], roles[2])

        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True

        await client.edit_channel_permissions(channel, member, overwrite)

        await client.logout()

client.run(config.tokens['barmaid'])
