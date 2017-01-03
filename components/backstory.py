import asyncio
import components.parts.commandWraps as wraps
from components.parts.discordModule import DiscordModule
from components.parts.discordModule import CommandError
from pubsub import pub
import random
import discord
import dataset
from stuf import stuf
import re
import datetime
import random

class backstory(DiscordModule):
    __prefix__ = "!"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "bckstry_add": self.add_item,
            "bckstry_del": self.remove_item,
            "bckstry_show": self.show_item,
            "bckstry_info": self.info,
            "bckstry_toggle": self.toggle_state
        }
        self.table = self.db['backstory']
        self.guilds = self.db['guilds']
        self.backstory = list(self.table.all())

        pub.subscribe(self, 'message')

    async def fire(self, message: discord.Message):
        if str(message.content).startswith(self.__prefix__):
            if str(message.content).split(' ')[0][1:] in self.__dispatcher__.keys():
                try:
                    await self.__dispatcher__[str(message.content).split(' ')[0][1:]](
                        message=message)
                except TypeError:
                    pass
                return

        if message.server:
            guild = self.guilds.find_one(guildId=message.server.id)
            if not guild:
                return

            if self.valid_channel(message):
                await self.send_backstory(message)

    async def send_backstory(self, message: discord.Message):
        for item in self.backstory:
            if item.key in message.clean_content:
                if random.randint(0, 100) < int(item.chance) and self.valid_backstory(
                        message, item):
                    await asyncio.sleep(random.randint(0,10), loop=self.client.loop)
                    await self.client.send_message(message.channel, item.text)
                    self.entry_time(item.key)
                    self.guild_time(message.server.id)

    @wraps.message_handler
    @wraps.is_owner
    async def toggle_state(self, message: discord.Message):
        guild = self.guilds.find_one(guildId=message.server.id)
        if not guild:
            entry = dict(guildId=message.server.id, backstoryChannel=message.channel.id)
            self.guilds.insert(entry)
            await self.client.send_message(message.channel, "I like it here~ I might feel " +
                                           "talkative from time to time. I hope that's okay " +
                                           "with everyone!")
        else:
            if guild.backstoryChannel:
                entry = dict(guildId=message.server.id, backstoryChannel=None)
                self.guilds.update(entry, ['guildId'])
                await self.client.send_message(message.channel, "You know, this isn't a nice " +
                                               "place after all. It doesn't feel safe to talk.")
            else:
                entry = dict(guildId=message.server.id, backstoryChannel=message.channel.id)
                self.guilds.update(entry, ['guildId'])
                await self.client.send_message(message.channel, "I like it here~ I might feel " +
                                               "talkative from time to time. I hope that's okay " +
                                               "with everyone!")

        await self.client.delete_message(message)

    patterns = {
        "add": re.compile(r'^!\w+ {([\w\s]+)} time=(\d+) chance=(\d+) {(.+)}$',
                          flags=re.IGNORECASE),
    }

    @wraps.message_handler
    @wraps.is_owner
    async def add_item(self, message: discord.Message):
        match = re.fullmatch(self.patterns['add'], message.clean_content)

        if match:
            entry = dict(
                key=match.group(1),
                delay=int(match.group(2)),
                chance=int(match.group(3)),
                text=match.group(4)
            )
            if self.table.find_one(key=match.group(1)):
                old = self.table.find_one(key=match.group(1))
                self.table.update(entry, ['key'])
                msg = ("I've updated my old backstory. For reference, it was:\n**Key**: {}\n"
                       "**Delay**: {}\n**Chance**: {}\n**Text**: {}").format(
                           old.key, old.delay, old.chance, old.text)
            else:
                self.table.insert(entry)
                msg = "I've memorized my new backstory. Thank you!"
            
            await self.client.send_message(message.channel, msg)
        else:
            await self.client.send_message(message.channel, ("Sorry, but I didn't understand " +
                                                             "that! The format for this command " +
                                                             "is `{} {{keyword}} time=# chance=# " +
                                                             "{{text to respond with}}`. Could you " +
                                                             "try again?").format(
                                                                 str(message.content).split(' ')[0]))
            raise CommandError("invalid format")

    @wraps.message_handler
    @wraps.is_owner
    async def remove_item(self, message: discord.Message):
        match = re.fullmatch(self.command_matchers['num'], message.clean_content)

        if match:
            item = self.table.find_one(id=match.group(1))
            if item:
                self.table.delete(id=match.group(1))
                msg = ("I've forgotten my old backstory. For reference, it was:\n**Key**: {}\n"
                       "**Delay**: {}\n**Chance**: {}\n**Text**: {}").format(
                           item.key, item.delay, item.chance, item.text)
            else:
                msg = "That key doesn't exist, sorry."
            await self.client.send_message(message.channel, msg)
            return
        else:
            match = re.fullmatch(self.command_matchers['any'], message.clean_content)
            if match:
                item = self.table.find_one(key=match.group(1))
                if item:
                    self.table.delete(key=match.group(1))
                    msg = ("I've forgotten my old backstory. For reference, it was:\n**Key**: {}\n"
                           "**Delay**: {}\n**Chance**: {}\n**Text**: {}").format(
                               item.key, item.delay, item.chance, item.text)
                else:
                    msg = "That key doesn't exist, sorry."
                await self.client.send_message(message.channel, msg)
                return


        await self.client.send_message(message.channel, "Sorry, but I didn't understand "
                                                        "that! The format for this command "
                                                        "is `{} #`. Could you try again?".format(
                                                            str(message.content).split(' ')[0]))
        raise CommandError("invalid format")

    @wraps.message_handler
    @wraps.is_owner
    async def show_item(self, message: discord.Message):
        match = re.fullmatch(self.command_matchers['num'], message.clean_content)

        if match:
            result = self.table.find_one(id=match.group(1))
        else:
            match = re.fullmatch(self.command_matchers['word'], message.clean_content)
            if match:
                result = self.table.find_one(key=match.groupd(1))
            else:
                result = None

        if result:
            await self.client.send_message(
                message.channel, "{}: {}".format(match.group(1), result.text))
        else:
            await self.client.send_message(message.channel, "Sorry, but I didn't understand "
                                           "that! The format for this command is `{} key`. Could "
                                           "you try again?".format(str(
                                               message.content).split(' ')[0]))
            raise CommandError("invalid format")

    @wraps.message_handler
    @wraps.is_owner
    async def info(self, message: discord.Message):
        pass


    def guild_time(self, guildId: int):
        entry = dict(guildId=guildId, backstoryTimestamp=datetime.datetime.now().timestamp())
        self.guilds.update(entry, ['guildId'])
        # self.backstory = random.shuffle(self.backstory)
    
    def entry_time(self, key: str):
        entry = dict(key=key, timestamp=datetime.datetime.now().timestamp())
        self.table.update(entry, ['key'])

    def valid_channel(self, message: discord.Message):
        guild = self.guilds.find_one(guildId=message.server.id)
        if not guild:
            return False
        if not guild.backstoryChannel:
            return False

        if guild.backstoryChannel == message.channel.id:
            try:
                return ((message.timestamp - datetime.datetime.fromtimestamp(
                    guild.backstoryTimestamp)) < datetime.timedelta(minutes=60))
            except AttributeError:
                return True
            except TypeError:
                return True
        else:
            return False

    def valid_backstory(self, message: discord.Message, story: stuf):
        try:
            return ((message.timestamp - datetime.datetime.fromtimestamp(story.timestamp))
                    < datetime.timedelta(minutes=int(story.delay)))
        except AttributeError:
            return True
        except TypeError:
            return True



