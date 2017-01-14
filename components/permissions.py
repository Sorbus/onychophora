import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord
import re

class Permissions(DiscordModule):
    """
        Various utility functions.
    """
    prefix = ";"

    class Cooldown(DiscordModule.DiscordCommand):
        word = "permission.cooldown"
        keys = ["cd", "cooldown"]
        desc = ["Sets the cooldown for a command."]
        example = ["%prefix%cd command seconds, %prefix%cd command seconds channel"]
        scheme = [("word", True), ("num", True), ("channel", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    