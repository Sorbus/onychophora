import discord
import asyncio
import config
import components
from pubsub import pub

class Bot:
    def __init__(self):
        self.config = config.Global()
        self.client = discord.Client()

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.client.run(self.config.token))
        self.loop.close() 

    async def send_message(self, destination, content=None, tts=None, embed=None):
        try:
            self.client.send_message(destination, content=None, tts=None, embed=None)
        except discord.errors.Forbidden:
            print("Insufficient permissions to send a message on {}.".format(destination.name))

bot = Bot()

@bot.client.event
async def on_ready():
    print('Logged in as {} ({}).'.format(bot.client.user.name, bot.client.user.id))
    print('Connected to {} servers.'.format(len(bot.client.servers)))
    print('Ready to serve, Mistress!')
    print('------')
    if bot.config.notify:
        for o in bot.config.owners:
            owner = await bot.client.get_user_info(o)
            await bot.send_message(owner, "I'm ready to serve you, Mistress!")

@bot.client.event
async def on_message(message: discord.Message):
    if message.author.id is not bot.client.user.id:
        pub.sendMessage('message', message=message)

@bot.client.event
async def on_message_delete(message: discord.Message):
    if message.author.id is not bot.client.user.id:
        pub.sendMessage('message_delete', message=message)

@bot.client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.id is not bot.client.user.id:
        pub.sendMessage('message_edit', before=before, after=after)

@bot.client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.id is not bot.client.user.id:
        pub.sendMessage('reaction_add', reaction=reaction, user=user)

@bot.client.event
async def on_server_join(server: discord.Server):
    pub.sendMessage('server_join', server=server)

@bot.client.event
async def on_server_remove(server: discord.Server):
    pub.sendMessage('server_remove', server=server)

@bot.client.event
async def on_voice_state_update(before: discord.Member, after: discord.Member):
    if after.id is not bot.client.user.id:
        pub.sendMessage('voice_status', before=before, after=after)

def main():
    modules = []
    modules.append(components.response.response(bot))

    bot.run()

if __name__ == '__main__':
    main()