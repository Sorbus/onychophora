import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class Logging(DiscordModule):
    """
        Options related to monitoring channel activity.
    """
    __prefix__ = ";"
    __value__ = "semicolon"
