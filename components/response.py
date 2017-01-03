import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class response(DiscordModule):
    __prefix__ = "."

    def __init__(self, bot):
        super().__init__(bot)
        pub.subscribe(self, 'message')

    async def fire(self, message: discord.Message):
        if "import yaml" in message.content:
            await self.send_and_delete(message.channel, "https://i.imgur.com/aoQt6mz.png", 15)
        elif "alot" in message.content:
            await self.send_and_delete(message.channel, "https://i.imgur.com/EJl6Os3.png", 15)
