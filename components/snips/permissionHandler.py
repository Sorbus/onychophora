import asyncio
from pubsub import pub
import discord
from datetime import datetime
from components.snips.errors import CommandError
from colorama import Fore, Back, Style

def permission_handler(s, message:discord.Message):
    """
    Checks if a command can be run.
    """

