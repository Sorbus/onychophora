import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class Response(DiscordModule):
    """
        Automatic responses to keywords.
        Unlike backstory they have no timer, and unlike quotes they're looser.
    """
    __prefix__ = "."

    def __init__(self, bot):
        super().__init__(bot)
        pub.subscribe(self, 'message')

    async def fire(self, message: discord.Message):
        pass
        # if "import yaml" in message.content:
        #     await self.send_and_delete(message.channel, "https://i.imgur.com/aoQt6mz.png", 15)
        # elif "alot" in message.content:
        #     await self.send_and_delete(message.channel, "https://i.imgur.com/EJl6Os3.png", 15)
