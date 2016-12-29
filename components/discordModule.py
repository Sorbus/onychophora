import asyncio
import re
import discord
from pubsub import pub

class DiscordModule(object):
    '''
        Barebones implementation for discord commands.
        Subclasses will end up reimplementing everything at present,
        but still a good idea for the future.
    '''
    __prefix__ = None
    # must be set to load
    __dispatcher__ = {}
    # should be set if used

    def __init__(self, bot):
        '''
            Must be implemented. Call super and register.
        '''
        self.config = bot.config
        self.client = bot.client
        self.loop = asyncio.get_event_loop()
        # pub.subscribe(self, 'message')

    def __call__(self, message):
        '''
            Only implemented if it takes a different input.
        '''
        self.loop.create_task(self.fire(message))

    async def fire(self, message: discord.Message):
        if str(message.content).startswith(self.__prefix__):
            if str(message.content).split(' ')[0][1:] in self.__dispatcher__.keys():
                await self.__dispatcher__[str(message.content).split(' ')[0][1:]](message)

    id_matcher = re.compile("<@!(\d{18})>")

    async def user_in_string(self, message: discord.Message, text: str):
        result = await self.users_in_string(message, text)
        try:
            return result[0]
        except IndexError:
            return []

    async def users_in_string(self, message: discord.Message, text: str):
        if message.mentions:
            return message.mentions
        d = list(filter(None, text.split(' ')))
        users = []
        for x in range(0,len(d) if len(d) < 3 else 3):
            for y in range(x+1,x+2):
                m = message.server.get_member_named(" ".join(d[x:y]))
                if m is not None:
                    if m not in users:
                        users.append(m)

        return users

    async def delete_after(self, message: discord.Message, sec):
        await asyncio.sleep(sec, loop=self.client.loop)
        await self.client.delete_message(message)