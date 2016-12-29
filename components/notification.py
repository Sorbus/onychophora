import asyncio
from .discordModule import DiscordModule
from pubsub import pub
import discord

class notification(DiscordModule):
    __prefix__ = ";"
