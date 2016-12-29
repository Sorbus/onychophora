import asyncio
from .discordModule import DiscordModule
from pubsub import pub
import discord

class response(DiscordModule):
    __prefix__ = "."

    def __init__(self, bot):
        super().__init__(bot)
        pub.subscribe(self, 'message')

    async def fire(self, message: discord.Message):
        if "import yaml" in message.content:
            msg = await self.client.send_message(message.channel, "https://i.imgur.com/aoQt6mz.png")
            await self.delete_after(message, 15)
        elif "alot" in message.content:
            msg = await self.client.send_message(message.channel, "https://i.imgur.com/EJl6Os3.png")
            await self.delete_after(message, 15)
