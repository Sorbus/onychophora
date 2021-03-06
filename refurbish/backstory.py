import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule
from components.snips.discordModule import CommandError
from pubsub import pub
import random
import discord
import dataset
import sqlalchemy
from stuf import stuf
import re
import datetime
import random

class Backstory(DiscordModule):
    """
        Intermittent responses to various keywords.
        Differentiated from reactions by being on timers.
    """
    __prefix__ = "!"
    __value__ = "exclaimation"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "bckstry_add": self.add_item,
            "bckstry_del": self.remove_item,
            "bckstry_show": self.show_item,
            "bckstry_info": self.info,
            "bckstry_toggle": self.toggle_state
        }

        try:
            self.table = self.db.load_table('backstory')
        except sqlalchemy.exc.NoSuchTableError:
            self.table = self.db.create_table('backstory', primary_id='key', primary_type='String')

            self.table.create_column('delay', sqlalchemy.INT)
            self.table.create_column('chance', sqlalchemy.INT)
            self.table.create_column('text', sqlalchemy.TEXT)
            self.table.create_column('timestamp', sqlalchemy.DATETIME)

            self.table.create_index(['keyword', 'guildId'])

        self.guilds = self.db['guilds']
        self.find_valid()

        pub.subscribe(self.process, 'message-other')
    
    async def process(self, **kwargs):
        if "message" in kwargs:
            message = kwargs['message']
            if message.server:
                guild = self.guilds.find_one(guildId=message.server.id)
                if not guild:
                    return

                if self.channel_ready(message):
                    await self.send_backstory(message)
        else:
            raise CommandError("handler not implemented in Backstory.process()")

    async def send_backstory(self, message: discord.Message):
        if self.timestamp < (message.timestamp - datetime.timedelta(minutes = 5)):
            self.find_valid()
        now = datetime.datetime.utcnow()
        for item in self.stories:
            if (
                    (len(item.key) < 6 and
                     item.key.lower() in message.clean_content.lower().split(" "))
                    or
                    (len(item.key) > 5 and
                     item.key.lower() in message.clean_content.lower())
                ):
                if random.randint(0, 100) < int(item.chance):
                    self.entry_time(item.key, now.timestamp())
                    self.guild_time(message.server.id, now.timestamp())
                    await asyncio.sleep(random.randint(0, 5), loop=self.client.loop)
                    await self.client.send_typing(message.channel)
                    await asyncio.sleep(random.randint(0, 5), loop=self.client.loop)
                    await self.client.send_message(message.channel, item.text)
                    return

    def find_valid(self):
        self.stories = list()
        self.timestamp = datetime.datetime.now()
        for item in self.table.all():
            if self.story_ready(self.timestamp, item):
                self.stories.append(item)

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
        "add": re.compile(r'^!\w+ {(.+)} time=(\d+) chance=(\d+) {(.+)}$',
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
                text=match.group(4),
                timestamp=0
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
            self.find_valid()
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
                self.find_valid()
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
                result = self.table.find_one(key=match.group(1))
            else:
                result = None

        if result and match:
            await self.client.send_message(
                message.channel, ("Here's the first item with that key:\n**Key**: {}\n"
                                  "**Delay**: {}\n**Chance**: {}\n**Text**: {}\n**Id**: {}").format(
                                      result.key, result.delay, result.chance, result.text,
                                      result.id))
        elif match:
            await self.client.send_message(message.channel, "Sorry, that's not a valid key")
        else:
            await self.client.send_message(message.channel, "Sorry, but I didn't understand "
                                           "that! The format for this command is `{} key`. Could "
                                           "you try again?".format(str(
                                               message.content).split(' ')[0]))
            raise CommandError("invalid format")

    @wraps.message_handler
    @wraps.is_owner
    async def info(self, message: discord.Message):
        stories = self.table.find(order_by='key')
        msg = "Here are the items I currently have in my backstory:\n"
        for item in stories:
            msg += "{} [{}] ".format(item.key, item.id)
            if len(msg) > 1800:
                await self.client.send_message(message.channel, msg)
                await asyncio.sleep(2, loop=self.client.loop)
                msg = ""
        if msg:
            await self.client.send_message(message.channel, msg)

    def guild_time(self, guildId: int, now: float):
        entry = dict(guildId=guildId, backstoryTimestamp=now)
        self.guilds.update(entry, ['guildId'])
    
    def entry_time(self, key: str, now: float):
        entry = dict(key=key, timestamp=now)
        self.table.update(entry, ['key'])

    def is_ready(self, now: datetime.datetime, then: datetime.datetime, minutes=0, seconds=0):
        pass

    def channel_ready(self, message: discord.Message):
        guild = self.guilds.find_one(guildId=message.server.id)
        if not guild:
            return False
        if not guild.backstoryChannel:
            return False

        if guild.backstoryChannel == message.channel.id:
            try:
                return (
                    datetime.datetime.fromtimestamp(
                        guild.backstoryTimestamp) < (message.timestamp - datetime.timedelta(
                            minutes=self.config.backstory.timer))
                )
            except AttributeError:
                return True
            except TypeError:
                return True
        else:
            return False

    def story_ready(self, now: datetime.datetime, story: stuf):
        try:
            return (
                datetime.datetime.fromtimestamp(story.timestamp) < (now - datetime.timedelta(minutes=story.delay))
            )
        except AttributeError:
            return True




