import asyncio
import re
import discord
from pubsub import pub

class command(object):
    def __init__(self, client: discord.Client, config):
        self.client = client
        self.config = config
        pub.subscribe(self, 'message')

    def __call__(self, message):
        print(message.content)
