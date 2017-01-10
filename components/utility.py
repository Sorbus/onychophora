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
    prefix = "~"
    value = "tilde"

    class Avatar(DiscordModule.DiscordCommand):
        word = "utility.avatar"
        keys = ["av", "avatar"]
        desc = ["Returns a link to the author or another user's avatar."]
        example = ["%prefix%av | %prefix%av @someone"]
        scheme = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            if len(tup):
                await self.client.send_message(message.channel, "{}'s avatar is:\n{}.".format(
                    tup[0].name, tup[0].avatar_url))
            else:
                await self.client.send_message(message.channel, "Your avatar is:\n{}.".format(
                    message.author.avatar_url))

    class UserDetails(DiscordModule.DiscordCommand):
        word = "utility.user"
        keys = ["user", "member"]
        desc = ["Returns details about the author or another user."]
        example = ["%prefix%user | %prefix%user @someone"]
        scheme = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class ChannelDetails(DiscordModule.DiscordCommand):
        word = "utility.channel"
        keys = ["ch", "channel"]
        desc = ["Returns details about this or another channel."]
        example = ["%prefix%ch | %prefix%ch #somewhere"]
        scheme = [("channel", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class ServerDetails (DiscordModule.DiscordCommand):
        word = "utility.channel"
        keys = ["server"]
        desc = ["Returns details about this server."]
        example = ["%prefix%server"]
        scheme = []

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
        word = "utility.savechat"
        keys = ["savechat"]
        desc = ["Saves the last X messages in chat."]
        example = ["%prefix%savechat 100"]
        scheme = [("num", True)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            pass

    class Test(DiscordModule.DiscordCommand):
        word = "utility.test"
        keys = ["test"]
        desc = ["Simple test command."]
        example = ["%prefix%test | %prefix%test @someone"]
        scheme = [("user", False)]

        async def fire(self, message: discord.Message, tup: tuple=None):
            if not tup:
                await self.client.send_message(
                    message.channel, "You're {}.".format(message.author.id))
            elif not tup[0]:
                await self.client.send_message(message.channel, "I don't know who that is.")
            else:
                await self.client.send_message(
                    message.channel, "That's {}".format(tup[0].id))
