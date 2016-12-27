import discord
import asyncio
import config
import components
from pubsub import pub

config = config.Global()
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {} ({}).'.format(client.user.name, client.user.id))
    print('Connected to {} servers.'.format(len(client.servers)))
    print('Ready to serve, Mistress!')
    print('------')
    if config.notify:
        for o in config.owners:
            owner = await client.get_user_info(o)
            await client.send_message(owner, "I'm ready to serve you, Mistress!")

@client.event
async def on_message(message: discord.Message):
    pub.sendMessage('message', message=message)

@client.event
async def on_message_delete(message: discord.Message):
    pub.sendMessage('message_delete', message=message)

@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    pub.sendMessage('message_edit', before=before, after=after)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    pub.sendMessage('reaction_add', reaction=reaction, user=user)

@client.event
async def on_server_join(server: discord.Server):
    pub.sendMessage('server_join', server=server)
    for owner in config.owners:
        await client.send_message(owner, "I was added to {}.".format(server.name))

@client.event
async def on_server_remove(server: discord.Server):
    pub.sendMessage('server_remove', server=server)
    for owner in config.owners:
        await client.send_message(owner, "I was removed from {}.".format(server.name))

@client.event
async def on_voice_state_update(before: discord.Member, after: discord.Member):
    pub.sendMessage('voice_status', before=before, after=after)

def main():
    command_module = components.command.command(client, config)
    event_module = components.event.events(client, config)

    client.run(config.token)


if __name__ == '__main__':
    main()