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
        self.help = {}
        self.load_modules()

        pub.subscribe(self.on_ready, 'ready')
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
                            and o.prefix is not None
                            and o.value is not None
                            and str(o.__name__) not in self.config.module_blacklist):      
                        self.modules.append(o(self))
                        if o.prefix in self.prefixes:
                            if self.prefixes[o.prefix] != o.value.lower():
                                print("Prefix conflict on {}: {} is not {}".format(
                                    o.prefix, o.value, self.prefixes[o.prefix]))
                        self.prefixes[o.prefix] = o.value.lower()
                        loaded += " {}".format(o.__name__)

        if not loaded:
            print("Mistress, I couldn't load any modules.")
            sys.exit()
        else:
            print("Loaded modules:{}.".format(loaded))
            # print(self.prefixes.keys())

    def add_user(self, member):
        self.users['nicks'][member.server.id][member.id] = member.name.lower()
        self.users['names'][member.server.id][member.id] = member.display_name.lower()

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

    def on_ready(self):
        self.prepare_users()
        self.client.loop.create_task(self.report())

    def prepare_users(self):
        self.users['nicks'] = {}
        self.users['names'] = {}

        for server in self.client.servers:
            self.users['nicks'][server.id] = {}
            self.users['names'][server.id] = {}
            self.add_users(server)

    async def report(self):
        print('Logged in as {} ({}).'.format(self.client.user.name, self.client.user.id))
        print('Connected to {} servers:'.format(len(self.client.servers)))
        for server in self.client.servers:
            print('\t{}: {} users, {} channels, owned by {}.'.format(
                server.name,
                len(server.members),
                len(server.channels),
                server.owner.name
            ))

        print('Ready to serve, Mistress!')
        print('------')
        if self.config.notify:
            for o in self.config.owners.keys():
                owner = await self.client.get_user_info(o)
                await self.client.send_message(owner, "I'm ready to serve you, {}!".format(
                    self.config.owners[o]))
