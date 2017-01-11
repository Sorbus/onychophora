import asyncio
from pubsub import pub
import discord
from datetime import datetime
from components.snips.errors import CommandError
from colorama import Fore, Back, Style
        
def isOwner(s, author: discord.User):
    if int(author.id) not in s.config.owners.keys():
        raise CommandError("restricted to bot owner")

def isServer(channel: discord.Channel):
    if channel.type is not discord.ChannelType.text:
        raise CommandError("must be run on a server")
 
def isAdmin(perms: discord.Permissions):
    if not perms.administrator:
        raise PermissionError()

def manageServer(perms: discord.Permissions):
    if not perms.manage_server:
        raise PermissionError()

def manageChannels(perms: discord.Permissions):
    if not perms.manage_channels:
        raise PermissionError()

def manageMessages(perms: discord.Permissions):
    if not perms.manage_messages:
        raise PermissionError()

def readMessageHistory(perms: discord.Permissions):
    if not perms.read_message_history:
        raise PermissionError()

def changeNickname(perms: discord.Permissions):
    if not perms.change_nickname:
        raise PermissionError()

def manageNicknames(perms: discord.Permissions):
    if not perms.manage_nicknames:
        raise PermissionError()

def manageRoles(perms: discord.Permissions):
    if not perms.manage_roles:
        raise PermissionError()

def mentionEveryone(perms: discord.Permissions):
    if not perms.mention_everyone:
        raise PermissionError()

def kickMembers(perms: discord.Permissions):
    if not perms.kick_members:
        raise PermissionError()

def banMembers(perms: discord.Permissions):
    if not perms.ban_members:
        raise PermissionError()

def createInstantInvite(perms: discord.Permissions):
    if not perms.create_instant_invite:
        raise PermissionError()

def impossible(perms: discord.Permissions):
    raise CommandError("command marked as impossible.")

permissions = {
    "isAdmin": isAdmin,
    "manageServer": manageServer,
    "manageChannels": manageChannels,
    "manageMessages": manageMessages,
    "readMessageHistory": readMessageHistory,
    "changeNickname": changeNickname,
    "manageNicknames": manageNicknames,
    "manageRoles": manageRoles,
    "mentionEveryone": mentionEveryone,
    "kickMembers": kickMembers,
    "banMembers": banMembers,
    "createInstantInvite": createInstantInvite,
    "impossible!": impossible
}

def permission_handler(s, message: discord.Message):
    """
    Checks if a command can be run.
    """
    if s.requires:
        if "isOwner" in s.requires:
            isOwner(s, message.author)
        if "isServer" in s.requires:
            isServer(message.channel)

        perms = message.author.permissions_in(message.channel)
        for item in s.requires:
            if item in permissions.keys():
                permissions[item](perms)