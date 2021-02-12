import os
import re
import discord
import configparser
from bot.commands import Command

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as: {0} - {1}".format(client.user.name, client.user.id))
    print("-" * 20)


@client.event
async def on_message(message):
    command = message.content
    if message.author == client.user:
        return
    # elif command == "!":
    #     return await message.channel.send(
    #         "<@{0}>, No command has been passed.".format(message.author.id)
    #     )
    elif command.startswith("!help_gicle"):
        return await message.channel.send('!gicle {IMAGE_URL, [MENTION1, MENTION2, ...]} [MESSAGE]\tSends you back a modified image\n!help_gicle\tDisplays this help')
    elif command.startswith("!gicle"):
        m = None
        if len(message.mentions) > 0:
            m = message.mentions
        command = re.sub(r"<@.*?>", "", command[6:], 0, re.MULTILINE)
        paths = await Command.gicle(command, message.channel, client.user, mentions=m)
        for p in paths:
            await message.channel.send(file=discord.File(p))
        # return await message.channel.send(file=discord.File(path))


# Set up the base bot
class DiscordBot(object):
    def __init__(self):
        self.token = None
        self.config = configparser.ConfigParser()

    def create_config(self):
        # Ask user for bot token
        self.token = input("Bot Token:")
        # Creates base config file
        self.config.add_section("DiscordBot")
        self.config.set("DiscordBot", "token", self.token)
        with open("{0}/{1}".format(os.getcwd(), "config.ini"), "w") as configfile:
            self.config.write(configfile)

    def get_token(self):
        self.config.read("{0}/{1}".format(os.getcwd(), "config.ini"))
        self.token = self.config.get("DiscordBot", "token")

    def set_token(self, token):
        self.config.read("{0}/{1}".format(os.getcwd(), "config.ini"))
        self.config.set("DiscordBot", "token", token)
        with open("{0}/{1}".format(os.getcwd(), "config.ini"), "w") as configfile:
            self.config.write(configfile)

    def run(self):
        client.run(self.token)
