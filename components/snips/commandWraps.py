import asyncio
from pubsub import pub
import discord
from datetime import datetime
from components.snips.errors import CommandError
from colorama import Fore, Back, Style
from .permissionHandler import *

def message_handler(function):
    """
    Print actions caused by messages.
    """

    async def wrapper(s, message: discord.Message):
        try:
            start = datetime.now()
            permission_handler(s, message)
            result = await function(self=s, message=message)
            if message.channel.type is discord.ChannelType.private:
                print(("{} {} | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Channel: direct message\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(),
                           message.author.name, message.author.id, message.content)
                     )
            elif message.channel.type is discord.ChannelType.group:
                print(("{} {} | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Channel: private group ({})\n\tMembers: {}\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.channel.id, message.content)
                     )
            elif message.channel.type is discord.ChannelType.text:
                print(("{} {} | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Server: {} [{}]\n\tChannel: {} [{}]\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.server.name, message.server.id,
                           message.channel.name, message.channel.id, message.content)
                     )
            return result
        except CommandError as err:
            if message.channel.type is discord.ChannelType.private:
                print((Fore.MAGENTA + "{} {} | Command errored after {:.8}s\n" +
                       Fore.MAGENTA + "\tUser: {} [{}]\n" + Fore.MAGENTA +
                       "\tChannel: direct message\n\tMessage: {}\n" + Fore.MAGENTA +
                       "\tError: {}" + Fore.RESET).format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.content, err.message)
                     )
            elif message.channel.type is discord.ChannelType.group:
                print((Fore.MAGENTA + "{} {} | Command errored after {:.8}s\n" +
                       Fore.MAGENTA + "\tUser: {} [{}]\n" + Fore.MAGENTA +
                       "\tChannel: private group ({})\n" + Fore.MAGENTA + "\tMembers: {}\n" +
                       Fore.MAGENTA + "\t" + "Message: {}\n" + Fore.MAGENTA + "\tError: {}" +
                       Fore.RESET).format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.channel.id, message.content, err.message)
                     )
            elif message.channel.type is discord.ChannelType.text:
                print((Fore.MAGENTA + "{} {} | Command errored after {:.8}s\n\t" +
                       Fore.MAGENTA + "User: {} [{}]\n\t" + Fore.MAGENTA + "Server: {} [{}]\n\t" +
                       Fore.MAGENTA + "Channel: {} [{}]\n\t" + Fore.MAGENTA + "Message: {}\n" +
                       Fore.MAGENTA + "\tError: {}" + Fore.RESET).format(
                           start.strftime("%H:%M:%S"), s.word,
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.server.name, message.server.id,
                           message.channel.name, message.channel.id, message.content, err.message)
                     )
        except PermissionError:
            pass
    return wrapper
