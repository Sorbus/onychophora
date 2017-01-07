import asyncio
from pubsub import pub
import discord
from datetime import datetime
from .discordModule import CommandError
from colorama import Fore, Back, Style

def message_handler(function):
    """
    Print actions caused by messages.
    """

    async def wrapper(s, message: discord.Message):
        try:
            start = datetime.now()
            result = await function(s, message=message)
            if message.channel.type is discord.ChannelType.private:
                print(("{} MessageTrigger | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Channel: direct message\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(),
                           message.author.name, message.author.id, message.content)
                     )
            elif message.channel.type is discord.ChannelType.group:
                print(("{} MessageTrigger | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Channel: private group ({})\n\tMembers: {}\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.channel.id, message.content)
                     )
            elif message.channel.type is discord.ChannelType.text:
                print(("{} MessageTrigger | Executed after {:.8}s\n\tUser: {} [{}]\n\t"+
                       "Server: {} [{}]\n\tChannel: {} [{}]\n\tMessage: {}").format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.server.name, message.server.id,
                           message.channel.name, message.channel.id, message.content)
                     )
            return result
        except CommandError as err:
            if message.channel.type is discord.ChannelType.private:
                print((Fore.MAGENTA + "{} MessageTrigger | Command errored after {:.8}s\n" +
                       Fore.MAGENTA + "\tUser: {} [{}]\n" + Fore.MAGENTA +
                       "\tChannel: direct message\n\tMessage: {}\n" + Fore.MAGENTA +
                       "\tError: {}" + Fore.RESET).format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.content, err.message)
                     )
            elif message.channel.type is discord.ChannelType.group:
                print((Fore.MAGENTA + "{} MessageTrigger | Command errored after {:.8}s\n" +
                       Fore.MAGENTA + "\tUser: {} [{}]\n" + Fore.MAGENTA +
                       "\tChannel: private group ({})\n" + Fore.MAGENTA + "\tMembers: {}\n" +
                       Fore.MAGENTA + "\t" + "Message: {}\n" + Fore.MAGENTA + "\tError: {}" +
                       Fore.RESET).format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.channel.id, message.content, err.message)
                     )
            elif message.channel.type is discord.ChannelType.text:
                print((Fore.MAGENTA + "{} MessageTrigger | Command errored after {:.8}s\n\t" +
                       Fore.MAGENTA + "User: {} [{}]\n\t" + Fore.MAGENTA + "Server: {} [{}]\n\t" +
                       Fore.MAGENTA + "Channel: {} [{}]\n\t" + Fore.MAGENTA + "Message: {}\n" +
                       Fore.MAGENTA + "\tError: {}" + Fore.RESET).format(
                           start.strftime("%H:%M:%S"),
                           (datetime.now() - start).total_seconds(), message.author.name,
                           message.author.id, message.server.name, message.server.id,
                           message.channel.name, message.channel.id, message.content, err.message)
                     )
    return wrapper

def is_server(function):
    """
    Only allow commands to be run on servers.
    """

    async def wrapper(s, **kwargs):
        if "message" in kwargs.keys():
            if kwargs["message"].channel.type is not discord.ChannelType.text:
                raise CommandError("must be run on a server")
            return await function(s, message=kwargs["message"])
        else:
            raise CommandError("unhandled input in commandWraps.is_server")
    return wrapper

def manage_channels(function):
    """
    Only allow commands to be run by people with this permission
    """

    async def wrapper(s, **kwargs):
        if "message" in kwargs.keys():
            if (kwargs["message"].author.permissions_in(kwargs["message"].channel)).manage_channels:
                raise CommandError("requires manage messages")
            return await function(s, message=kwargs["message"])
        else:
            raise CommandError("unhandled input in commandWraps.manage_channels")
    return wrapper

def manage_server(function):
    """
    Only allow commands to be run by people with this permission
    """

    async def wrapper(s, **kwargs):
        if "message" in kwargs.keys():
            if (kwargs["message"].author.permissions_in(kwargs["message"].channel)).manage_server:
                raise CommandError("requires manage messages")
            return await function(s, message=kwargs["message"])
        else:
            raise CommandError("unhandled input in commandWraps.manage_channels")
    return wrapper

def is_owner(function):
    """
    Restrict command to owner
    """
    async def wrapper(s, **kwargs):
        if "message" in kwargs.keys():
            if int(kwargs["message"].author.id) not in s.config.owners.keys():
                raise CommandError("restricted to owner")
            return await function(s, message=kwargs["message"])
        else:
            raise CommandError("unhandled input in commandWraps.manage_channels")
    return wrapper
