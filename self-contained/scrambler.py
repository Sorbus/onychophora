import discord
import asyncio
import re
import random
import yaml
import atexit
import datetime
from helpers import Config

client = discord.Client()
config = Config()

try:
    with open('names.yml', 'r') as stream:
        data = yaml.load(stream)
except FileNotFoundError:
    data = {}
    data['names'] = {}
    data['original'] = {}

name_prefix = ['septentional','brabbling','jargogled', 'glimmering',
               'yemeles', 'whilom', 'nubivagant', 'pamphagous', 'crawling',
               'dream-beset', 'woe betide', 'plead for', 'cry for', 'weep for',
               'mourn for', 'a memory of', 'another', 'the only', 'yet to be']
name_suffix = ['of the beyond', 'of the tower', 'of the ending'
               'of the void', 'of the sea', 'of the air', 'of the fire',
               'the saturnist', 'of Dream', 'the apricious',
               'the clockmaker', 'of regret', 'perhaps', 'of another',
               'in memory', 'in knowledge', 'of the library']

def create_change(member):
    if random.randint(0,9):
        name = member.display_name
    else:
        name = ''.join(random.sample(
            member.display_name, len(member.name)))

    if random.randint(0, 2):
        suf = ' {}'.format(random.choice(name_suffix))
    else:
        suf = ''

    if random.randint(0, 2):
        pre = '{} '.format(random.choice(name_prefix))
    else:
        pre = ''

    if (len(name) + len(suf) + len(pre)) > 32:
        over = (len(name) + len(suf) + len(pre)) - 32

        if len(name) > over:
            name = name[:(len(name)-over)]
        else:
            suf = ''

    return ('{}{}{}'.format(pre,name,suf)).title().replace('  ', ' ')

def save():
    with open('names.yml', 'w') as stream:
        yaml.dump(data, stream)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # server = None
    # for s in client.servers:
    #     if int(s.id) == 239675999959121921:
    #         server = s
    # await client.change_nickname(server.me, "barmaid")

@client.event
async def on_message(message: discord.Message):
    await scramble(message.author, message.server, message)

async def scramble(member: discord.Member, server: discord.Server, message: discord.Message):
    try:
        if int(server.id) != 239675999959121921:
            return
        if message.content.startswith(".randomname"):
            data['names'][member.id] = create_change(member)
            if not member.id in data['original']:
                data['original'][member.id] = member.display_name
            print('changed {} -> {}'.format(member.name, data['names'][member.id]))
            old_name = str(member.display_name)
            await client.change_nickname(member, data['names'][member.id])
            save()
            await client.add_reaction(message, '👍')
            await client.add_reaction(message, '👎')
            res = await client.wait_for_reaction(['👍', '👎'], message=message,
                                                 timeout=300, user=message.author)
            await client.remove_reaction(message, '👍', message.server.me)
            await client.remove_reaction(message, '👎', message.server.me)
            if res:
                if res.reaction.emoji == '👍':
                    print("{} accepted {}".format(member.name, member.nick))
                elif res.reaction.emoji == '👎':
                    data['names'].pop(member.id)
                    print("{} rejected {}".format(member.name, member.nick))
                    await client.change_nickname(member, old_name)
                    save()
        elif message.content.startswith(".revertname"):
            if member.id in data['original']:
                await client.change_nickname(member, data['original'][member.id])
                await client.send_message(
                    message.channel, "Your name has been reverted to what it was before you "
                                     "first used `.randomname`.")
            else:
                await client.send_message(message.channel, "You haven't used `.randomname` yet.")
        elif message.content.startswith(".restorename"):
            if member.id in data['names']:
                await client.change_nickname(member, data['names'][member.id])
                await client.send_message(
                    message.channel, "Your name has been reverted to what it was the last "
                                     "time you used `.randomname`.")
            else:
                await client.send_message(message.channel, "You haven't used `.randomname` yet.")

    except discord.errors.Forbidden:
        pass
    except discord.errors.HTTPException:
        pass

client.run(config.tokens['barmaid'])