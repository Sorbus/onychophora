import discord
import asyncio
import sys
import re
from helpers import Config
import types
import yaml
from random import choice

client = discord.Client()
config = Config()

compliments = yaml.load(open('data/compliment.yml', newline=''))

@client.event
async def on_ready():
    """
    report on startup
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    client.connection.http = client.http
    client.connection.parse_msg_re_add = types.MethodType(parse_msg_re_add, client.connection)
    client.connection.parse_message_reaction_add = types.MethodType(parse_message_reaction_add,
                                                            client.connection)

def parse_message_reaction_add(self, data):
    client.connection.loop.create_task(self.parse_msg_re_add(data))

async def parse_msg_re_add(self, data):
    message = self._get_message(data['message_id'])

    if message is None:
        mhmm = await self.http.get_message(data['channel_id'], data['message_id'])
        message = self._create_message(channel=self.get_channel(data['channel_id']), **mhmm)

    if message is not None:
        emoji = self._get_reaction_emoji(**data.pop('emoji'))
        reaction = discord.utils.get(message.reactions, emoji=emoji)

        is_me = data['user_id'] == self.user.id

        if not reaction:
            reaction = discord.Reaction(
                message=message, emoji=emoji, me=is_me, **data)
            message.reactions.append(reaction)
        else:
            reaction.count += 1
            if is_me:
                reaction.me = True

        channel = self.get_channel(data['channel_id'])
        member = self._get_member(channel, data['user_id'])

        self.dispatch('reaction_add', reaction, member)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if (message.channel.name in ['the-council', 'mod-chat', 'elses-web', 'crypt'] and
       message.channel.permissions_for(message.author).manage_messages):
        if message.content.startswith('.vote '):
            msg = await client.send_message(message.channel,
                                            "@here\nVoting: {}\nClick on a reaction to vote."
                                            "\nTap ❔ or ❓ to tally."
                                            "".format(message.content[6:]))

            await client.add_reaction(msg, '👍')
            await client.add_reaction(msg, '👎')
            await client.add_reaction(msg, '✋')
            await client.add_reaction(msg, '❔')
            await client.pin_message(msg)
            await client.delete_message(message)
            print('started vote for {}'.format(message.author.name))

        if message.content.startswith('.tally '):
            match = re.search('(\d{18}) ?([^$]+)?', message.content)
            if not match:
                return

            msg = None
            try:
                msg = await client.get_message(message.channel, match.group(1))
            except discord.errors.NotFound:
                # print("not found in {}".format(message.channel.name))
                for c in msg.server.channels:
                    try:
                        msg = await client.get_message(c, match.group(1))
                        break
                    except discord.errors.NotFound:
                        pass
                        # print("not found in {}".format(c.name))
                    except discord.errors.Forbidden:
                        pass
                        # print("cannot access {}".format(c.name))
            if not msg:
                await client.send_message(message.channel, "Sorry, I couldn't find that message.")
                return

            await tally_votes(msg, message.channel, match.group(2))

    if (message.clean_content.lower().startswith("compliment")
        and not message.channel.is_private):
        if message.clean_content.lower() == 'compliment me':
            await client.send_message(message.channel, choice(compliments['first']).replace('%user%', message.author.mention))
            print('complimented {}'.format(message.author.name))
        elif len(message.mentions) is 1:
            if message.mentions[0] is message.author:
                await client.send_message(message.channel, choice(compliments['first']).replace('%user%', message.author.mention))
                print('complimented {}'.format(message.author.name))
            else:
                await client.send_message(message.channel, choice(compliments['second']).replace('%source%', message.author.mention).replace('%target%', message.mentions[0].mention))
                print('complimented {} for {}'.format(message.mentions[0].name, message.author.name))

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.bot:
        return
    if not reaction.message.channel.name in ['the-council', 'mod-chat', 'crypt']:
        return

    if reaction.emoji == '❓' and reaction.message.channel.permissions_for(user).manage_messages:
        await tally_votes(reaction.message, reaction.message.channel)
        await client.remove_reaction(reaction.message, reaction.emoji, user)
    elif reaction.emoji == '❔':
        await tally_votes(reaction.message, user)
        await client.remove_reaction(reaction.message, reaction.emoji, user)


async def tally_votes(message: discord.Message, channel: discord.Channel, word: str=None):
    match2 = re.search('Voting: ([^$]+)\n', message.content)
    if match2:
        subject = match2.group(1)
    else:
        subject = word if word else "unidentified subject"
    if not subject:
        subject = "unidentified subject"

    votes = {}
    voters = []
    for item in message.reactions:
        if item.emoji in ['❓', '❔']:
            break
        #if item.emoji in votes:
        users = await client.get_reaction_users(item, limit=50)
        if message.server.me in users:
            votes[item.emoji] = item.count - 1
        else:
            votes[item.emoji] = item.count

        for u in users:
            if not u.bot and not int(u.id) in voters:
                voters.append(int(u.id))

    notvoted = []

    for u in message.server.members:
        if message.channel.permissions_for(u).read_messages:
            if not u.bot and not int(u.id) in voters:
                notvoted.append(u.name)

    await report_votes(message, channel, notvoted, subject,
                       ', '.join(['%s: %s' % (key, value) for (key, value) in votes.items()]))

async def report_votes(message: discord.Message, channel: discord.Channel,
                       notvoted: list, subject: str, results: str):
    if notvoted:
        if len(notvoted) < 10:
            await client.send_message(channel,
                                      ("Tallying votes for {}:\n{}.\n"
                                       "Waiting on votes from: {}."
                                      ).format(subject, results, ', '.join(notvoted)))
        else:
            await client.send_message(channel,
                                      ("Tallying votes for {}:\n{}.\n"
                                       "Waiting on votes from more than ten people."
                                      ).format(subject, results))
    else:
        await client.send_message(channel,
                                  ("Tallying votes for {}:\n{}.\n"
                                   "All users have voted.").format(subject, results))
        await client.unpin_message(message)

client.run(config.tokens['barmaid'])
