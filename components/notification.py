import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class notification(DiscordModule):
    __prefix__ = ";"
