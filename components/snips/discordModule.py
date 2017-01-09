import asyncio
from .commandWraps import *

import re
import inspect
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
        self.help = bot.help
        self.users = bot.users
        self.db = bot.db
        self.loop = asyncio.get_event_loop()
        self.commands=[]

        for name, obj in inspect.getmembers(self):
            if inspect.isclass(obj):
                if issubclass(obj, DiscordModule.DiscordCommand):
                    if (obj.__word__ and
                            obj.__keys__ and
                            obj.__desc__ and
                            obj.__example__):
                        self.commands.append(obj(self))
                        for key in obj.__keys__:
                            self.help['{}{}'.format(self.__prefix__, key)] = (
                                "**{}**:\n**Keys**: {}\n**Description**: {}\n**Usage**: {}".format(
                                    obj.__word__,
                                    ' '.join(obj.__keys__),
                                    obj.__desc__,
                                    obj.__example__
                                ).replace('%prefix%', self.__prefix__)
                            )

    def __call__(self, message):
        '''
            Only implemented if it takes a different input.
            Sorts input so that fire can do magic to it.
        '''
        #self.loop.create_task(self.fire(message=message))

    async def fire(self, message: discord.Message):
        raise NotImplementedError

    class DiscordCommand(object):
        __word__ = None # identifies command for permissions
        __keys__ = None # should be an array
        __desc__ = None # says what the command does
        __example__ = None # an example of how to use it
        __scheme__ = None # if present, used to generate the regex
        __regex__ = None # regex which determines whether input is valid

        def __init__(self, module):
            self.config = module.config
            self.client = module.client
            self.users = module.users
            self.db = module.db
            self.loop = asyncio.get_event_loop()
            for key in self.__keys__:
                pub.subscribe(self, 'message.{}.{}'.format(module.__value__, key))
            if self.__scheme__:
                self.__regex__ = DiscordModule.make_regex(self.__scheme__)

        def __call__(self, message):
            self.loop.create_task(self.process(message=message))

        @message_handler
        async def process(self, message):
            match = re.fullmatch(self.__regex__, message.content)
            if not match:
                raise CommandError("invalid format")
            else:
                i = 0
                gathered = []
                if self.__scheme__:
                    for item in match.groups():
                        if not item:
                            break
                        if self.__scheme__[i][0] == 'channel':
                            channel = await self.client.get_channel(item)
                            gathered.append(channel)
                        elif self.__scheme__[i][0] == 'user':
                            user = None
                            if re.fullmatch(r'^\d{18}$', item):
                                user = await self.client.get_user_info(int(item))
                            else:
                                for id, name in self.users['names'][message.server.id].items():
                                    if name == item.lower():
                                        found = id
                                        break
                                for id, name in self.users['nicks'][message.server.id].items():
                                    if name == item.lower():
                                        found = id
                                        break
                                if found:
                                    for member in message.server.members:
                                        if member.id == found:
                                            user = member
                                    if not user:
                                        user = await self.client.get_user_info(id)
                            gathered.append(user)
                        elif self.__scheme__[i][0] == 'server':
                            gathered.append(await self.client.get_server(item))
                        else:
                            gathered.append(item)

                        i += 1
                    await self.fire(message, tuple(gathered))
                else:
                    await self.fire(message, match)

        async def fire(self, message: discord.Message, match, tup: tuple=None):
            raise NotImplementedError

    @staticmethod
    def make_regex(scheme: list):
        '''
        Assemble a regex expression from a list of tuples of the form:
        [
            (name, mandatory)
        ]
        Note: because of the way these are constructed, weird things will
                happen if more than one item is optional. No error handling
                related to this is provided at this time. I should probably
                add it in, just in case ...
        '''
        parts = {
            "server": r'(\d{18})',
            "channel": r'(?:<#)?((?<=<#)\d{18}(?=>)|\w+)>?',
            "user": r'(?:<@)?(?:"(?=.+"))?((?<=<@)\d{18}(?=>)|(?<=").+(?=")|\w+)>?"?',
            "num": r'(\d+)',
            "word": r'(?:"(?=.+"))?((?<=").+(?=")|\w+)"?',
            "all": r'([^$]+)'
        }

        prep = r'^\S+'

        for item in scheme:
            if item[0] in parts.keys():
                prep += r'(?: {})'.format(parts[item[0]])
                prep += r'' if item[1] else r'?'
            else:
                raise Exception

        prep += r'$'

        return re.compile(prep, flags=re.IGNORECASE)

