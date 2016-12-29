import asyncio
from .discordModule import DiscordModule
from pubsub import pub
import discord

class startup(DiscordModule):
    __prefix__ = ";"

    def __init__(self, bot):
        super().__init__(bot)
        pub.subscribe(self, 'ready')

    def __call__(self):
        self.loop.create_task(self.fire())

    async def fire(self):
        print('Logged in as {} ({}).'.format(self.client.user.name, self.client.user.id))
        print('Connected to {} servers:'.format(len(self.client.servers)))
        for s in self.client.servers:
            print('\t{}: {} users, {} channels, owned by {}.'.format(
                s.name,
                len(s.members),
                len(s.channels),
                s.owner.name
            ))

        print('Ready to serve, Mistress!')
        print('------')
        if self.config.notify:
            for o in self.config.owners:
                owner = await self.client.get_user_info(o)
                await self.client.send_message(owner, "I'm ready to serve you, Mistress!")

    