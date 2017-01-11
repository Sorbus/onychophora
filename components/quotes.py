import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule
from components.snips.discordModule import CommandError
import components.snips.permissionHandler as permissionHandler
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
    prefix = "."
    value = "period"

    def __init__(self, bot):
        self.db = bot.db
        try:
            self.table = self.db.load_table('quotes')
        except sqlalchemy.exc.NoSuchTableError:
            self.table = self.db.create_table('quotes')

            self.table.create_column('keyword', sqlalchemy.TEXT)
            self.table.create_column('guildId', sqlalchemy.INT)
            self.table.create_column('authorId', sqlalchemy.INT)
            self.table.create_column('authorName', sqlalchemy.TEXT)
            self.table.create_column('text', sqlalchemy.TEXT)

            self.table.create_index(['keyword', 'guildId'])
        super().__init__(bot)

    class Quote(DiscordModule.DiscordCommand):
        def __init__(self, bot):
            super().__init__(bot)
            self.table = bot.table

    class AddQuote(Quote):
        word = "quote.add"
        keys = ("dot")
        desc = "Add a quote to the database."
        example = "%prefix%. keyword quote"
        scheme = (("word", True), ("all", True))
        requires = ("isServer")

        async def fire(self, message: discord.Message, tup: tuple=None):
            self.table.insert(dict(
                authorId=message.author.id,
                authorName=message.author.name,
                guildId=message.server.id,
                keyword=tup[0],
                text=tup[1]
                ))

            await self.client.send_message(message.channel, "I've memorized your quote!")

    class GetQuote(Quote):
        word = "quote.get"
        keys = ("dotdot")
        desc = "Retrieve a quote."
        example = "%prefix%.. keyword"
        scheme = (("all", True))
        requires = ("isServer")

        async def fire(self, message: discord.Message, tup: tuple=None):
            found = list(self.table.find(guildId=message.server.id, keyword=tup[0]))
            if not found:
                raise CommandError("no results found")
            await self.client.send_message(message.channel, ":mega: {}".format(
                random.choice(found).text))

    class UpdateQuote(Quote):
        word = "quote.update"
        keys = ("changequote", "chqu")
        desc = "Modify an existing quote."
        example = "%prefix%chqu id quote"
        scheme = (("num", True), ("word", True))
        requires = ("isServer")

        async def fire(self, message: discord.Message, tup: tuple=None):
            found = self.table.find_one(guildId=message.server.id, id=tup[0])
            if found:
                if (found.id == message.author.id or
                        permissionHandler.isOwner(self, message.author) or
                        permissionHandler.manageMessages(message.author).permissions_in(
                            message.channel)):
                    self.table.update(dict(
                        id=tup[0],
                        authorId=message.author.id,
                        authorName=message.author.name,
                        text=tup[1]
                        ), ['id'])
                    await self.send_and_delete(message.channel, "I've updated your quote! " +
                                               "But just in case, here's the old version:" +
                                               "\n```\n{}\n```".format(found.text))
            else:
                await self.send_and_delete(message.channel,
                                           "I'm sorry, I couldn't find that quote. " +
                                           "Could you check the id?", 10)

    class DeleteQuote(Quote):
        word = "quote.delete"
        keys = ("delq", "qdel")
        desc = [("Delete a quote by id or keyword. Id is recommended; "
                 "keywords will choose a random quote under that keyword to delete.")]
        example = ["%prefix%delq key"]
        scheme = (("word", True))
        requires = ["isServer"]

        async def fire(self, message: discord.Message, tup: tuple=None):
            if tup[0].isDigit():
                pass
            

    class ListQuotes(Quote):
        word = "quote.list"
        keys = ["listquotes","liqu"]
        desc = ["List all quotes on a keyword."]
        example = ["%prefix%liqu keyword"]
        scheme = [("all", True)]
        requires = ["isServer"]

        async def fire(self, message: discord.Message, tup: tuple=None):
            found = list(self.table.find(guildId=message.server.id, keyword=tup[0]))
            if not found:
                raise CommandError("no results found")

            response = 'The following quotes are registered under "{}":\n'.format(tup[0])
            for q in found:
                if len(q.text) > 64:
                    response += "- ({.id}) {:.64} ...\n".format(
                        q, q.text.replace('\n', ' ').replace('\r', ''))
                else:
                    response += "- ({.id}) {:.64}\n".format(
                        q, q.text.replace('\n', ' ').replace('\r', ''))
                if len(response) > 1800:
                    await self.client.send_message(message.channel, response)
                    response = ''

            await self.client.send_message(message.channel, response)
