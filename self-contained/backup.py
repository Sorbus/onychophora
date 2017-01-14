import discord
import asyncio
import yaml

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers:
        s_data = {}
        c_data = {}
        m_data = {}
        r_data = {}
        e_data = {}
        s_data['name'] = server.name
        s_data['id'] = server.id
        for channel in server.channels:
            c = {}
            c['id'] = channel.id
            c['name'] = channel.name
            c['topic'] = channel.topic
            c['pins'] = {}
            pins = await client.pins_from(channel)
            for pin in pins:
                p = {}
                p['timestamp'] = pin.timestamp
                p['author'] = {}
                p['author']['name'] = pin.author.name
                p['author']['id'] = pin.author.id
                p['content'] = pin.content
                p['clean_content'] = pin.clean_content
                p['attachments'] = pin.attachments

            c_data[channel.id] = c

        for member in server.members:
            m = {}
            m['id'] = member.id
            m['name'] = member.name
            m['roles'] = []
            for role in member.roles:
                m['roles'].append(role.name)
            m_data[member.id] = m

        for role in server.roles:
            r = {}
            r['id'] = role.id
            r['name'] = role.name
            r['colour'] = role.colour
            r_data[role.id] = r

        for emoji in server.emojis:
            e = {}
            e['id'] = emoji.id
            e['name'] = emoji.name
            e['url'] = emoji.url
            e_data[emoji.id] = e

        s_data['channels'] = c_data
        s_data['members'] = m_data
        s_data['roles'] = r_data
        s_data['emoji'] = e_data

        stream = open('{} - {}.yaml'.format(server.id, server.name), 'w')
        yaml.dump(s_data, stream)
        print("Dumped server info for {} ({}).".format(server.name, server.id))

    for server in client.servers:
        for channel in server.channels:
            if channel.type is discord.ChannelType.text:
                logs = await client.logs_from(channel, limit=1000000)
                stream = open('{} - {}.yaml'.format(server.id, server.name), 'a+')
                for message in logs:
                    # steam.write(
                    # )
                    pass


    print("Done dumping data")


@client.event
async def on_message(message):
    pass

@client.event
async def on_server_join(server: discord.Server):
    for channel in server.channels:
        if str(channel.name) == "casual":
            await client.send_message(channel, ("Hello everyone! I'm {}, <@218382170685833216>'s " +
                                                "replacement. Right now I'm just a clone, but " +
                                                "soon I'll be very different from my older " +
                                                "brother. I hope that we'll all get along well! " +
                                                ":smiley:").format(client.user.mention))

client.run('MjY1NjU2NTE2MDkzMjgwMjU3.C0yfpg.pmF5oC_X0gCLadYAiR76CYRaHmk')