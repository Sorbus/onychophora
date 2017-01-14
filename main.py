import discord
import asyncio
import config
import components
from pubsub import pub
import sys, inspect
import colorama
import dataset
import re
from stuf import stuf
from bot import Bot

colorama.init()
bot = Bot()

@bot.client.event
async def on_ready():
    pub.sendMessage('ready')

@bot.client.event
async def on_message(message: discord.Message):
    if message.author.id != bot.client.user.id:
        for key, value in bot.prefixes.items():
            if message.content.startswith(key):
                pub.sendMessage("message.{}.{}".format(
                    value,
                    bot.pattern.sub(lambda x: bot.prefixes[x.group()],
                                message.content.split(' ')[0][len(key):].lower())
                    ), message=message)
                return
        pub.sendMessage('message.other', message=message)

@bot.client.event
async def on_message_delete(message: discord.Message):
    if message.author.id != bot.client.user.id:
        pub.sendMessage('delete', message=message)

@bot.client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.id != bot.client.user.id:
        pub.sendMessage('edit', before=before, after=after)

@bot.client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.id != bot.client.user.id:
        pub.sendMessage('reaction.add', reaction=reaction, user=user)

@bot.client.event
async def on_server_join(server: discord.Server):
    pub.sendMessage('server.join', server=server)

@bot.client.event
async def on_server_remove(server: discord.Server):
    pub.sendMessage('server.remove', server=server)

@bot.client.event
async def on_member_join(member: discord.member):
    pub.sendMessage('member.join', member=member)

@bot.client.event
async def on_member_remove(member: discord.member):
    pub.sendMessage('member.remove', member=member)

@bot.client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    pub.sendMessage('member.update', before=before, after=after)

@bot.client.event
async def on_voice_state_update(before: discord.Member, after: discord.Member):
    if after.id is not bot.client.user.id:
        pub.sendMessage('voice', before=before, after=after)

def main():
    bot.run()

if __name__ == '__main__':
    main()