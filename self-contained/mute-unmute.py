import discord
import asyncio
import argparse
import sys
import yaml

parser = argparse.ArgumentParser(description='Mute or unmute a user.')
parser.add_argument('server', metavar='serverId', type=int, help='the target server')
parser.add_argument('user', metavar='userId', type=int, help='the user\'s id')
parser.add_argument('-r', '--role', type=str, help='the role to add/remove', default="muted")
parser.add_argument('-un', '--unmute', dest='mute', help='unmute the user', action='store_false')
parser.set_defaults(mute=True)

class Config(object):

    config_path = "data/test_config.yml"

    def __init__(self, path=config_path):
        configfile = yaml.load(open(path, newline=''))

        self.tokens = configfile['tokens']

args = parser.parse_args()
client = discord.Client()
config = Config()

@client.event
async def on_ready():
    """
    report on startup
    """

    server = None
    user = None
    role = None

    for item in client.servers:
        if int(item.id) == args.server:
            server = item

    if not server:
        print("Could not find server")
        await client.logout()

    for item in server.members:
        if int(item.id) == args.user:
            user = item

    if not user:
        print("Could not find user")
        await client.logout()

    for item in server.role_hierarchy:
        if str(item.name) == args.role:
            role = item

    if not role:
        print("Could not find role")
        await client.logout()

    if args.mute:
        await client.add_roles(user, role)
        print("Added [{.name}] to [{.name}]".format(role, user))
    else:
        await client.remove_roles(user, role)
        print("Removed [{.name}] from [{.name}]".format(role, user))


    await client.logout()

client.run(config.tokens['barmaid'])
