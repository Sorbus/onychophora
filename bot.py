import discord
import asyncio
import config
import components
from pubsub import pub
import sys, inspect
import colorama
import dataset
import sqlalchemy
from stuf import stuf

class Bot:
    def __init__(self):
        self.config = config.Global()
        self.client = discord.Client()
        self.db = dataset.connect('sqlite:///' + self.config.files['database'], row_type=stuf)
        self.modules = []
        self.prefixes = {}
        self.users = {}
        self.load_modules()

        pub.subscribe(self.prepare_users, 'ready')
        pub.subscribe(self.add_user, 'member.join')
        pub.subscribe(self.remove_user, 'member.remove')
        pub.subscribe(self.update_user, 'member.update')
        pub.subscribe(self.add_users, 'server.join')
        pub.subscribe(self.remove_users, 'server.remove')

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

    def add_user(self, member):
        self.users['nicks'][member.server.id][member.id] = member.name
        self.users['names'][member.server.id][member.id] = member.display_name

    def remove_user(self, member):
        self.users['nicks'][member.server.id].pop(member.id)
        self.users['names'][member.server.id].pop(member.id)

    def update_user(self, before, after):
        self.add_user(after)

    def add_users(self, server):
        for member in server.members:
            self.add_user(member)

    def remove_users(self, server):
        for member in server.members:
            self.remove_user(member)

    def prepare_users(self):
        self.users['nicks'] = {}
        self.users['names'] = {}

        for server in self.client.servers:
            self.users['nicks'][server.id] = {}
            self.users['names'][server.id] = {}
            self.add_users(server)
