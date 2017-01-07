import discord
import asyncio
import config
import components
from pubsub import pub
import sys, inspect
import colorama
import dataset
from stuf import stuf

class Bot:
    def __init__(self):
        self.config = config.Global()
        self.client = discord.Client()
        self.db = dataset.connect('sqlite:///' + self.config.files['database'], row_type=stuf)
        self.modules = []
        self.prefixes = {}
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
                    if (issubclass(o, components.snips.discordModule.DiscordModule)
                            and o.__prefix__ is not None
                            and o.__value__ is not None
                            and str(o.__name__) not in self.config.module_blacklist):      
                        self.modules.append(o(self))
                        if o.__prefix__ in self.prefixes:
                            if self.prefixes[o.__prefix__] != o.__value__.lower():
                                print("Prefix conflict on {}: {} is not {}".format(
                                    o.__prefix__, o.__value__, self.prefixes[o.__prefix__]))
                        self.prefixes[o.__prefix__] = o.__value__.lower()
                        loaded += " {}".format(o.__name__)

        if not loaded:
            print("Mistress, I couldn't load any modules.")
            sys.exit()
        else:
            print("Loaded modules:{}.".format(loaded))
            # print(self.prefixes.keys())

colorama.init()
bot = Bot()

@bot.client.event
async def on_ready():
    pub.sendMessage('ready')

@bot.client.event
async def on_message(message: discord.Message):
    if message.author.id != bot.client.user.id:
        pub.sendMessage('message-all', message=message)
        for key, value in bot.prefixes.items():
            if message.content.startswith(key):
                pub.sendMessage("message-{}".format(value), message=message)
                return
        pub.sendMessage('message-other', message=message)

@bot.client.event
async def on_message_delete(message: discord.Message):
    if message.author.id != bot.client.user.id:
        pub.sendMessage('message_delete', message=message)

@bot.client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.id != bot.client.user.id:
        pub.sendMessage('message_edit', before=before, after=after)

@bot.client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.id != bot.client.user.id:
        pub.sendMessage('reaction_add', reaction=reaction, user=user)

@bot.client.event
async def on_server_join(server: discord.Server):
    pub.sendMessage('server_join', server=server)

@bot.client.event
async def on_server_remove(server: discord.Server):
    pub.sendMessage('server_remove', server=server)

@bot.client.event
async def on_member_join(member: discord.member):
    pub.sendMessage('member_join', member=member)

@bot.client.event
async def on_member_remove(member: discord.member):
    pub.sendMessage('member_remove', member=member)

@bot.client.event
async def on_voice_state_update(before: discord.Member, after: discord.Member):
    if after.id is not bot.client.user.id:
        pub.sendMessage('voice_status', before=before, after=after)

def main():
    bot.run()

if __name__ == '__main__':
    main()