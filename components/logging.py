import asyncio
from .discordModule import DiscordModule
from pubsub import pub
import discord

class logging(DiscordModule):
    __prefix__ = ";"
