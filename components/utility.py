import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord
import re

class Utility(DiscordModule):
    """
        Various utility functions.
    """
    __prefix__ = "~"
    __value__ = "tilde"

    class Avatar(DiscordModule.DiscordCommand):
        __word__ = "utility.avatar"
        __keys__ = ["av", "avatar"]
        __desc__ = ["Returns a link to the author or another user's avatar."]
        __example__ = ["%prefix%av | %prefix%av @someone"]
        __scheme__ = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            if len(tup):
                await self.client.send_message(message.channel, "{}'s avatar is:\n{}.".format(
                    tup[0].name, tup[0].avatar_url))
            else:
                await self.client.send_message(message.channel, "Your avatar is:\n{}.".format(
                    message.author.avatar_url))

    class UserDetails(DiscordModule.DiscordCommand):
        __word__ = "utility.user"
        __keys__ = ["user", "member"]
        __desc__ = ["Returns details about the author or another user."]
        __example__ = ["%prefix%user | %prefix%user @someone"]
        __scheme__ = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class ChannelDetails(DiscordModule.DiscordCommand):
        __word__ = "utility.channel"
        __keys__ = ["ch", "channel"]
        __desc__ = ["Returns details about this or another channel."]
        __example__ = ["%prefix%ch | %prefix%ch #somewhere"]
        __scheme__ = [("channel", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class ServerDetails (DiscordModule.DiscordCommand):
        __word__ = "utility.channel"
        __keys__ = ["server"]
        __desc__ = ["Returns details about this server."]
        __example__ = ["%prefix%server"]
        __scheme__ = []

        async def fire(self, message: discord.Message, tup: tuple=None):
            server = message.server
            result = ("`Name:` {}\n`Id:` {}\n`Owner:` {} ({})\n`Icon:`"
                    "https://discordcdn.com/icons/{}/{}.jpg\n`Created:` {}\n".format(
                        server.name,
                        server.id,
                        server.owner.name,
                        server.owner.id,
                        server.id,
                        server.icon,
                        server.created_at
                        )
                    )
            result += "`Members:` {}\n`Roles:` {}\n ".format(
                len(server.members),
                len(server.role_hierarchy),
            )


            await self.client.send_message(message.channel, result)

    class SaveChat(DiscordModule.DiscordCommand):
        __word__ = "utility.savechat"
        __keys__ = ["savechat"]
        __desc__ = ["Saves the last X messages in chat."]
        __example__ = ["%prefix%savechat 100"]
        __scheme__ = [("num", True)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class Test(DiscordModule.DiscordCommand):
        __word__ = "utility.test"
        __keys__ = ["test"]
        __desc__ = ["Simple test command."]
        __example__ = ["%prefix%test | %prefix%test @someone"]
        __scheme__ = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            if not tup:
                await self.client.send_message(
                    message.channel, "You're {}.".format(message.author.id))
            elif not tup[0]:
                await self.client.send_message(message.channel, "I don't know who that is.")
            else:
                await self.client.send_message(
                    message.channel, "That's {}".format(tup[0].id))
