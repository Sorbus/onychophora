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
    __value__ = None
    '''
        Examples:
        ~: tilde
        !: exclaimation

    '''
    __dispatcher__ = {}
    # should be set if used

    def __init__(self, bot):
        '''
            Must be implemented. Call super and register.
        '''
        self.config = bot.config
        self.client = bot.client
        self.db = bot.db
        self.loop = asyncio.get_event_loop()
        pub.subscribe(self, 'message-{}'.format(self.__value__))

    def __call__(self, message):
        '''
            Only implemented if it takes a different input.
            Sorts input so that fire can do magic to it.
        '''

        self.loop.create_task(self.fire(message=message))

    async def fire(self, **kwargs):
        if "message" in kwargs:
            message = kwargs['message']
            if str(message.content).startswith(self.__prefix__):
                if str(message.content).split(' ')[0][1:] in self.__dispatcher__.keys():
                    try:
                        await self.__dispatcher__[str(message.content).split(' ')[0][1:]](message=message)
                    except TypeError:
                        pass
        else:
            raise CommandError("handler not implemented in DiscordModule.fire()")

    async def user_in_string(self, message: discord.Message, text: str):
        result = await self.users_in_string(message, text)
        try:
            return result[0]
        except IndexError:
            return False

    async def users_in_string(self, message: discord.Message, text: str):
        if message.mentions:
            return message.mentions
        d = list(filter(None, text.split(' ')))
        users = []
        for x in range(0,len(d) if len(d) < 3 else 3):
            for y in range(x+1,x+2):
                print("trying...")
                m = await message.server.get_member_named(" ".join(d[x:y]))
                print("I tried")
                if m is not None:
                    if m not in users:
                        users.append(m)

        return users

    async def send_and_delete(self, channel: discord.Channel, message: str, sec: int):
        msg = await self.client.send_message(channel, message)
        await asyncio.sleep(sec, loop=self.client.loop)
        await self.client.delete_message(msg)

    command_matchers = {
        "id": re.compile(r'^[^ ]+ (\d{18})', flags=re.IGNORECASE),
        "any": re.compile(r'^[^ ]+ ([\w\d]+|"[^\n]+")', flags=re.IGNORECASE),
        "num": re.compile(r'^[^ ]+ ([\d]+)', flags=re.IGNORECASE),
        "all": re.compile(r'^[^ ]+ ([^$]+)$', flags=re.IGNORECASE),
        "word": re.compile(r'^[^ ]+ ([\w]+|"[\w ]+")', flags=re.IGNORECASE),
        "any_all": re.compile('', flags=re.IGNORECASE),
        "any_num": re.compile('', flags=re.IGNORECASE)
        
    }

    async def parse_args(self, message: discord.Message, format: tuple):
        pass


class FormatError(Exception):
    """
    Exception raised when a string doesn't match the command format
    """

    def __init__(self, message):
        self.message = message

class CommandError(Exception):
    """
    Exception raised when a command occurs on an inappropriate channel
    """

    def __init__(self, message):
        self.message = message
