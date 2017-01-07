import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule
from components.snips.discordModule import CommandError
import components.interactiveGames.database
from pubsub import pub
import random
import discord
import dataset
from stuf import stuf
import re
import datetime
import random

class TextGame(DiscordModule):
    """
        Interactive fiction
    """
    #__prefix__ = ">> "
    #__value__ = "prompt"

    def __init__(self, bot):
        super().__init__(bot)

    @wraps.message_handler
    @wraps.is_owner
    async def toggle_state(self, message: discord.Message):
        pass



