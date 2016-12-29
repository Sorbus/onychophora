import asyncio
from .discordModule import DiscordModule
from pubsub import pub
import discord

class help(DiscordModule):
    __prefix__ = "-"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "help": self.help, "h": self.help
        }

        pub.subscribe(self, 'message')

    async def help(self, message: discord.Message):
        message = (
            "Hello, {}!".format(message.author.name, self.client.)
        )

        await self.client.send_message(message.author, message)