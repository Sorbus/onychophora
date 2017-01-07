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

class Quotes(DiscordModule):
    """
        Allows users to store and retrieve quotes.
    """
    __prefix__ = "."
    __value__ = "period"

    def __init__(self, bot):
        super().__init__(bot)
        
        try:
            self.table = self.db.load_table('quotes')
        except sqlalchemy.exc.NoSuchTableError:
            self.table = self.db.create_table('quotes', primary_id='keyword', primary_type='String')

            self.table.create_column('guildId', sqlalchemy.INT)
            self.table.create_column('authorId', sqlalchemy.INT)
            self.table.create_column('authorName', sqlalchemy.TEXT)
            self.table.create_column('text', sqlalchemy.TEXT)

            self.table.create_index(['keyword', 'guildId'])

        self.__dispatcher__ = {
            ".": self.add_quote,
            "..": self.get_quote,
            "delq": self.del_quote, "qdel": self.del_quote,
            "listquotes": self.list_quotes, "liqu": self.list_quotes,
            "changequote": self.change_quote, "chqu": self.change_quote
        }

        pub.subscribe(self, 'message')

    @wraps.message_handler
    @wraps.is_server
    async def add_quote(self, message: discord.Message):
        content = str(message.clean_content).split(' ')[1:]
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

            await self.client.send_message(message.channel, ":mega: {}".format(random.choice(found).text))
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
                message += "- ({}) {:128} ...\n".format(q.keyword, q.text)
            else:
                message += "- ({}) {:128}\n".format(q.keyword, q.text)

        await self.client.send_message(message.channel, response)