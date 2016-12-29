import discord
import asyncio
import config
import components
from pubsub import pub
import sys, inspect

class Bot:
    def __init__(self):
        self.config = config.Global()
        self.client = discord.Client()
        self.modules = []
        self.load_modules()

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.client.run(self.config.token))
        self.loop.close() 

    def load_modules(self):
        loaded = ""
        for name, obj in inspect.getmembers(components):
            for n, o in inspect.getmembers(obj):
                if inspect.isclass(o):
                    if (issubclass(o, components.discordModule.DiscordModule)
                        and o.__prefix__ is not None):
                        self.modules.append(o(self))
                        loaded += " {}".format(o.__name__)
        
        if not loaded:
            print("Mistress, I couldn't load any modules.")
            sys.exit()
        else:
            print("Loaded modules:{}.".format(loaded))

bot = Bot()

@bot.client.event
async def on_ready():
    pub.sendMessage('ready')

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
    bot.run()

if __name__ == '__main__':
    main()