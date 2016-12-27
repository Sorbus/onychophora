import discord
import asyncio
import re
from pubsub import pub

class notification(object):
    def __init__(self, bot):
        self.bot = bot
        pub.subscribe(self.removed, 'server_remove')
        pub.subscribe(self.added, 'server_added')

    def __call__(self, first):
        pass

    def added(self, server):
        asyncio.ensure_future(self.added_a(server))

    def removed(self, server):
        asyncio.ensure_future(self.removed_a(server))

    async def removed_a(self, server):
        for o in self.bot.config.owners:
            owner = await self.bot.client.get_user_info(o)
            await self.bot.send_message(owner, "I was removed from {}.".format(server.name))

    async def added_a(self, server):
        for o in self.bot.config.owners:
            owner = await self.bot.client.get_user_info(o)
            await self.bot.send_message(owner, "I was added to {}.".format(server.name))
