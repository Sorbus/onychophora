import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord
from colorama import Fore, Back, Style

class Startup(DiscordModule):
    """
        Things to do after the bot has connected to Discord.
    """
    __prefix__ = ";"
    __value__ = "semicolon"

    def __init__(self, bot):
        super().__init__(bot)
        pub.subscribe(self.run, 'ready')

    def run(self):
        self.loop.create_task(self.ready())

    async def ready(self):
        print('Logged in as {} ({}).'.format(self.client.user.name, self.client.user.id))
        print('Connected to {} servers:'.format(len(self.client.servers)))
        for server in self.client.servers:
            print('\t{}: {} users, {} channels, owned by {}.'.format(
                server.name,
                len(server.members),
                len(server.channels),
                server.owner.name
            ))

        print('Ready to serve, Mistress!')
        print('------')
        if self.config.notify:
            for o in self.config.owners.keys():
                owner = await self.client.get_user_info(o)
                await self.client.send_message(owner, "I'm ready to serve you, {}!".format(
                    self.config.owners[o]))

