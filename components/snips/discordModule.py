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
    prefix = None
    # must be set to load
    dispatcher = {}
    # should be set if used

    def __init__(self, bot):
        '''
            Must be implemented. Call super and register.
        '''
        self.config = bot.config
        self.client = bot.client
        self.prefixes = bot.prefixes
        self.pattern = bot.pattern
        self.help = bot.help
        self.users = bot.users
        self.db = bot.db
        self.loop = asyncio.get_event_loop()
        self.commands=[]

        for name, obj in inspect.getmembers(self):
            if inspect.isclass(obj):
                if issubclass(obj, DiscordModule.DiscordCommand):
                    if (obj.word is not None and
                            obj.keys is not None and
                            obj.desc is not None and
                            obj.example is not None):
                        self.commands.append(obj(self))
                        for key in obj.keys:
                            self.help['{}{}'.format(self.prefix, key)] = (
                                "**{}**:\n**Keys**: {}\n**Description**: {}\n**Usage**: {}".format(
                                    obj.word,
                                    ' '.join(obj.keys),
                                    obj.desc,
                                    obj.example
                                ).replace('%prefix%', self.prefix)
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
        word = None # identifies command for permissions
        keys = None # should be an array
        desc = None # says what the command does
        example = None # an example of how to use it
        scheme = None # if present, used to generate the regex
        regex = None # regex which determines whether input is valid
        requires = None # array. if set, only allow users with this permission to run the command

        def __init__(self, module):
            self.config = module.config
            self.client = module.client
            self.users = module.users
            self.db = module.db
            self.loop = asyncio.get_event_loop()
            for key in self.keys:
                pub.subscribe(self, 'message.{}.{}'.format(
                    module.pattern.sub(lambda x: module.prefixes[x.group()], module.prefix),
                    module.pattern.sub(lambda x: module.prefixes[x.group()], key)
                    ))
            if self.scheme:
                self.regex = DiscordModule.make_regex(self.scheme)

        def __call__(self, message):
            self.loop.create_task(self.process(message=message))

        @message_handler
        async def process(self, message: discord.Message):
            match = re.fullmatch(self.regex, message.content)
            if not match:
                raise CommandError("invalid format")
            else:
                i = 0
                gathered = []
                if self.scheme:
                    for item in match.groups():
                        if not item:
                            break
                        if self.scheme[i][0] == 'channel':
                            channel = await self.client.get_channel(item)
                            gathered.append(channel)
                        elif self.scheme[i][0] == 'user':
                            user = None
                            if len(message.mentions) is 1:
                                user = message.mentions[0]
                            if not user and re.fullmatch(r'^\d{18}$', item):
                                print(int(item))
                                user = message.server.get_member(item)
                            if not user:
                                found = None
                                for id, name in self.users['names'][message.server.id].items():
                                    if name == item.lower():
                                        found = id
                                        break
                                for id, name in self.users['nicks'][message.server.id].items():
                                    if name == item.lower():
                                        found = id
                                        break
                                if found:
                                    user = message.server.get_member(found)
                                    if not user:
                                        user = await self.client.get_user_info(id)
                                else:
                                    raise CommandError("invalid username")
                            gathered.append(user)
                        elif self.scheme[i][0] == 'server':
                            gathered.append(await self.client.get_server(item))
                        else:
                            gathered.append(item)

                        i += 1
                    await self.fire(message, tuple(gathered))
                else:
                    await self.fire(message, match)

        async def fire(self, message: discord.Message, match, tup: tuple=None):
            raise NotImplementedError

        async def send_and_delete(self, channel: discord.Channel, message: str, sec: int=False):
            msg = await self.client.send_message(channel, message)
            if sec:
                self.loop.create_task(self.wait_to_delete(msg, sec))

        async def wait_to_delete(self, message: discord.Message, sec: int):
            await asyncio.sleep(sec, loop=self.client.loop)
            await self.client.delete_message(message)

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
                print(item)
                print(scheme)
                raise ValueError

        prep += r'$'

        return re.compile(prep, flags=re.IGNORECASE)

