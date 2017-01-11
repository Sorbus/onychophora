import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule
from components.snips.discordModule import CommandError
from pubsub import pub
import random
import discord
import dataset
from stuf import stuf
import sys

class Administration(DiscordModule):
    """
        Various owner-only commands for bot management.
    """
    __prefix__ = "."
    __value__ = "period"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "sleep": self.shutdown
        }

        pub.subscribe(self, 'message')

    @wraps.message_handler
    @wraps.is_owner
    async def shutdown(self, message: discord.Message):
        """
            Turns the bot off.
        """
        await self.client.send_message(message.channel, "*yawn* Just ... gimme a moment, "
                                                        "I need ta lie down for a while ...")
        if not message.channel.is_private:
            await self.client.delete_message(message)
        await asyncio.sleep(5, loop=self.client.loop)
        sys.exit()
