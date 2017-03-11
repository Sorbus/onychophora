import discord
import asyncio
import yaml

class Config(object):

    config_path = "data/test_config.yml"

    def __init__(self, path=config_path):
        configfile = yaml.load(open(path, newline=''))

        self.tokens = configfile['tokens']

client = discord.Client()
config = Config()

river_colors = ['EE8A26', 'E58E36', 'DB9146', 'D29556', 'C89866', 'BF9C75', 'B59F85', 'ACA395', 'A2A6A5' '99AAB5']

cobra_colors = ['EB6263', 'E26A6C', 'D97275', 'D07A7E', 'C78287', 'BD8A90', 'B49299', 'AB9AA2', 'A2A2AB', '99AAB5']

@client.event
async def on_ready():
    """
    report on startup
    """

    server = None
    river = None
    cobra = None

    for item in client.servers:
        if int(item.id) == 239675999959121921:
            server = item

    if not server:
        print("Could not find server")
        await client.logout()

    for item in server.role_hierarchy:
        if str(item.name) == "river splitters":
            river = item
        if str(item.name) == "laser cobras":
            cobra = item

    if not river or not cobra:
        print("Could not find role")
        await client.logout()

    for i in range(0,12):
        print("{} -> {}\t\t{} -> {}".format(
            river.colour, river_colors[i], cobra.colour, cobra_colors[i]
        ))

        await client.edit_role(server, river, color=discord.Color(river_colors[i]))
        await client.edit_role(server, cobra, color=discord.Color(cobra_colors[i]))

        await asyncio.sleep(60, loop=client.loop)

    await client.logout()

client.run(config.tokens['barmaid'])
