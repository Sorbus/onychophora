import asyncio
import components.parts.commandWraps as wraps
from components.parts.discordModule import DiscordModule
from components.parts.discordModule import CommandError
from pubsub import pub
import random
import discord
import dataset
from stuf import stuf

class found(DiscordModule):
    __prefix__ = "."

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            ".": self.add_quote,
            "..": self.get_quote,
            "delq": self.del_quote, "qdel": self.del_quote,
            "listquotes": self.list_quotes, "liqu": self.list_quotes,
            "changequote": self.change_quote, "chqu": self.change_quote
        }
        self.table = self.db['quotes']

        pub.subscribe(self, 'message')

    @wraps.message_handler
    @wraps.is_server
    async def add_quote(self, message: discord.Message):
        content = str(message.content).split(' ')[1:]
        if len(content) < 2:
            raise CommandError("not enough arguments")

        self.table.insert(dict(
            authorId=message.author.id,
            authorName=message.author.name,
            guildId=message.server.id,
            keyword=content[0].upper(),
            text=' '.join(content[1:])
        ))

        await self.client.send_message(message.channel, "I've memorized your quote!")

    @wraps.message_handler
    @wraps.is_server
    async def get_quote(self, message: discord.Message):
        try:
            key = str(message.content).split(' ')[1].upper()

            found = list(self.table.find(guildId=message.server.id, keyword=key))
            
            if not found:
                raise CommandError("no results found")

            await self.client.send_message(message.channel, random.choice(found).text)
        except IndexError:
            pass

    @wraps.message_handler
    async def change_quote(self, message: discord.Message):
        pass

    @wraps.message_handler
    async def del_quote(self, message: discord.Message):
        pass
    
    @wraps.message_handler
    async def list_quotes(self, message: discord.Message):
        #if len(str(message.content).split(' ')) = 3
        key = str(message.content).split(' ')[1].upper()

        found = list(self.table.find(guildId=message.server.id, keyword=key))
        
        if not found:
            raise CommandError("no results found")

        response = ""
        for q in found:
            if q.text > 128:
                message += "- ({}) {:128} ...\n".format(q.id, q.text)
            else:
                message += "- ({}) {:128}\n".format(q.id, q.text)

        await self.client.send_message(message.channel, response)