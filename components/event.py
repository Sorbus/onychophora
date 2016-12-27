import asyncio
import re
import discord
from pubsub import pub

class event(object):
    def __init__(self, client: discord.Client, config):
        self.client = client
        self.config = config
        pub.subscribe(self.removed, 'server_remove')
        pub.subscribe(self.added, 'server_added')

    def __call__(self, message):
        pass

    def removed(self, server):
        # for o in self.config.owners:
        #     owner = await self.client.get_user_info(o)
        #     await self.client.send_message(owner, "I was removed from {}.".format(server.name))
        pass

    def added(self, server):
        # for o in self.config.owners:
        #     owner = await client.get_user_info(o)
        #     await self.client.send_message(owner, "I was added to {}.".format(server.name))
        pass

