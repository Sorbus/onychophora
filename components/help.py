import asyncio
import components.snips.commandWraps as wraps
from components.snips.discordModule import DiscordModule as DiscordModule
from pubsub import pub
import discord

class Help(DiscordModule):
    """
        Handles help messages and suchlike
    """
    __prefix__ = "-"

    def __init__(self, bot):
        super().__init__(bot)

        self.__dispatcher__ = {
            "help": self.help, "h": self.help
        }

        pub.subscribe(self, 'message')

    @wraps.message_handler
    async def help(self, message: discord.Message):
        owner = await self.client.get_user_info(list(self.config.owners.keys())[0])
        response = await self.tease_line(message, owner)
        response += (
            "I have a variety of functions, including:\n\n" +
            "- Falling over on the ground.\n" +
            "- Not actually doing what I'm supposed to.\n" +
            "- Being cute."
        )

        msg = await self.client.send_message(message.author, response)
        #await self.client.add_reaction(msg, ":heart:")

    async def tease_line(self, message: discord.Message, owner: discord.User):
        response = ""
        if int(message.author.id) in self.config.owners.keys():
            return ("Hello, {}! I hope that you're having a wonderful day.\n\n".format(
                self.config.owners[int(message.author.id)]) +
                    "I would explain who I am, but you already know that~\n\n"
                   )
        if int(message.author.id) in self.config.favored.keys():

            response += "Hello, **{}**! I'm **{}**.\n\n".format(
                self.config.favored[int(message.author.id)], self.client.user.name)
        else:
            response += "Hello, **{}**! I'm **{}**.\n\n".format(
                message.author.name, self.client.user.name)

        response += "I'm a bot written by **Else** and owned by **{}**.".format(owner.name)
        if str(self.client.user.name) is not "onychophora":
            response += "\n(I'm running on *Onychophora*, but that's not my name right now)\n\n"
        else:
            response += "\n\n"

        return response
