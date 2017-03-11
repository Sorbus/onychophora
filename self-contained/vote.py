import discord
import asyncio
import sys
import re
from helpers import Config

client = discord.Client()
config = Config()

@client.event
async def on_ready():
    """
    report on startup
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message: discord.Message):
    if not message.channel.name in ['the-council', 'elses-web', 'crypt']:
        return

    if message.channel.permissions_for(message.author).manage_messages:
        if message.content.startswith('.vote '):
            msg = await client.send_message(message.channel,
                                            "@here\nVoting: {}\n(Click on a reaction to vote.)".format(
                                                message.content[6:]
                                            ))

            await client.add_reaction(msg, '👍')
            await client.add_reaction(msg, '👎')
            await client.add_reaction(msg, '✋')
            await client.pin_message(msg)
            await client.delete_message(message)

        if message.content.startswith('.tally '):
            match = re.search('(\d{18}) ?([^$]+)?', message.content)
            if not match:
                return

            msg = None
            try:
                msg = await client.get_message(message.channel, match.group(1))
            except discord.errors.NotFound:
                # print("not found in {}".format(message.channel.name))
                for c in message.server.channels:
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

            match2 = re.search('Voting: ([^$]+)\n', msg.content)
            if match2:
                subject = match2.group(1)
            else:
                try:
                    subject = match.group(2)
                except IndexError:
                    subject = "unidentified subject"
            if not subject:
                subject = "unidentified subject"

            votes = {}
            voters = []
            for item in msg.reactions:
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

            for u in msg.server.members:
                if msg.channel.permissions_for(u).read_messages:
                    if not u.bot and not int(u.id) in voters:
                        notvoted.append(u.name)

            if notvoted:
                if len(notvoted) < 10:
                    await client.send_message(message.channel,
                                            ("Tallying votes for {}:\n{}.\n"
                                            "Waiting on votes from: {}.").format(subject,
                                                ', '.join(['%s: %s' % (key, value) for (key, value) in votes.items()]),
                                                ', '.join(notvoted)
                                            ))
                else:
                    await client.send_message(message.channel,
                                            ("Tallying votes for {}:\n{}.\n"
                                            "Waiting on votes from more than ten people.").format(subject,
                                                ', '.join(['%s: %s' % (key, value) for (key, value) in votes.items()]),
                                            ))
            else:
                await client.send_message(message.channel,
                                        ("Tallying votes for {}:\n{}.\n"
                                        "All users have voted.").format(subject,
                                            ', '.join(['%s: %s' % (key, value) for (key, value) in votes.items()])
                                        ))
                await client.unpin_message(msg)

client.run(config.tokens['barmaid'])
