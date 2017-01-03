import asyncio
import components.parts.commandWraps as wraps
from components.parts.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class logging(DiscordModule):
    __prefix__ = ";"
