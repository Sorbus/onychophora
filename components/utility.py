import asyncio
import components.parts.commandWraps as wraps
from components.parts.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class utility(DiscordModule):
    __prefix__ = "~"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "avatar": self.avatar, "av": self.avatar,
            "userinfo": self.user_details, "usi": self.user_details,
            "channelinfo": self.channel_details, "chi": self.channel_details,
            "serverinfo": self.server_details, "sei": self.server_details,
            "savechat": self.save_chat,
            "test": self.test
        }

        pub.subscribe(self, 'message')

    @wraps.message_handler
    async def avatar(self, message: discord.Message):
        await self.client.send_message(message.channel, message.author.avatar_url)

    @wraps.message_handler
    async def user_details(self, message: discord.Message):
        pass

    @wraps.message_handler
    async def channel_details(self, message: discord.Message):
        pass

    @wraps.message_handler
    async def server_details(self, message: discord.Message):
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

    @wraps.message_handler
    async def save_chat(self, message: discord.Message):
        pass

    @wraps.message_handler
    async def test(self, message: discord.Message):
        user = await self.user_in_string(message, message.content[6:])
        if not user:
            await self.client.send_message(message.channel, "I don't know who that is.")
        else:
            await self.client.send_message(message.channel, user.id)
