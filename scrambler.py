import discord
import asyncio
import re
import random
import yaml
import atexit
import datetime

client = discord.Client()

try:
    with open('names.yml', 'r') as stream:
        data = yaml.load(stream)
except FileNotFoundError:
    data = {}
    data['names'] = {}
    data['cooldowns'] = {}
    data['blacklist'] = []

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
        new_name = member.display_name
    else:
        new_name = ''.join(random.sample(
            member.display_name, len(member.display_name)))

    if random.randint(0, 2):
        suf = ' {}'.format(random.choice(name_suffix))
    else:
        suf = ''

    if random.randint(0, 2):
        pre = '{} '.format(random.choice(name_prefix))
    else:
        pre = ''

    if (len(new_name) + len(suf) + len(pre)) > 32:
        over = (len(new_name) + len(suf) + len(pre)) - 32

        if len(new_name) > over:
            new_name = new_name[:over]
        else:
            suf = ''

    return ('{}{}{}'.format(pre,new_name,suf)).title()

def save():
    with open('names.yml', 'w') as stream:
        yaml.dump(data, stream)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message: discord.Message):
    await scramble(message.author, message.server, message)

async def scramble(member: discord.Member, server: discord.Server, message: discord.Message):
    try:
        if random.randint(0,9) is not 0:
            return
        if (int(server.id) == 239675999959121921 and
                member.id not in data['blacklist']):
            if member.id not in data['names'].keys():
                data['names'][member.id] = create_change(member)
                data['cooldowns'][member.id] = datetime.datetime.now()
                print('changed {} -> {}'.format(member.name, data['names'][member.id]))
                await client.change_nickname(member, data['names'][member.id])
                save()
                await client.add_reaction(message, '👍')
                await client.add_reaction(message, '👎')
                await client.add_reaction(message, '💀')
                res = await client.wait_for_reaction(['👍', '👎', '💀'], message=message,
                                                     timeout=60, user=message.author)
                await client.remove_reaction(message, '👍', message.server.me)
                await client.remove_reaction(message, '👎', message.server.me)
                await client.remove_reaction(message, '💀', message.server.me)
                if res:
                    if res.reaction.emoji is '👍':
                        pass
                    elif res.reaction.emoji is '👎':
                        data['names'].pop(member.id)
                        save()
                    elif res.reaction.emoji is '💀':
                        data['names'].pop(member.id)
                        save()
                
            else:
                try:
                    if (data['cooldown'][member.id] > (datetime.datetime.now() - datetime.timedelta(minutes=7))):
                        return
                except KeyError:
                    pass
                if str(member.name) != str(data['names'][member.id]):
                    print('restored {} -> {}'.format(member.name, data['names'][member.id]))
                    data['cooldown'][member.id] = datetime.datetime.now()
                    await client.change_nickname(member, data['names'][member.id])
    except discord.errors.Forbidden:
        pass

client.run('MjY1NjU2NTE2MDkzMjgwMjU3.C0yfpg.pmF5oC_X0gCLadYAiR76CYRaHmk')