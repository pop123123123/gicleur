import os
import random
import pyttsx3
import tempfile
import re
import discord
import configparser
import asyncio
from bot.commands import Command

client = discord.Client()
engine = pyttsx3.init()


@client.event
async def on_ready():
    print("Logged in as: {0} - {1}".format(client.user.name, client.user.id))
    print("-" * 20)


@client.event
async def on_message(message):
    command = message.content
    if message.author == client.user:
        return
    elif command.startswith("!help_gicle"):
        return await message.channel.send(
            "!gicle {IMAGE_URL, [MENTION1, MENTION2, ...]} [MESSAGE]\tSends you back a modified image\n!help_gicle\tDisplays this help"
        )
    elif command.startswith("!gicle"):
        m = None
        if len(message.mentions) > 0:
            m = message.mentions
        command = re.sub(r"<@.*?>", "", command[6:], 0, re.MULTILINE)
        paths = await Command.gicle(command, message.channel, client.user, mentions=m)
        await asyncio.gather(
            *[message.channel.send(file=discord.File(p)) for p in paths]
        )
        # return await message.channel.send(file=discord.File(path))


def get_source(member):
    fp = tempfile.NamedTemporaryFile(suffix=".mp3")
    path = fp.name
    fp.close()
    msg = member.nick if member.nick is not None else member.name
    engine.save_to_file(msg + "ah trayz envi de G clay", path)
    engine.runAndWait()
    return path


@client.event
async def on_voice_state_update(member, before, after):
    if client.user != member and after is not None and member.voice is not None:
        if random.randint(0, 10) == 0:
            voiceClient = await member.voice.channel.connect()
            path = get_source(member)
            voiceClient.play(discord.FFmpegPCMAudio(path))
            while voiceClient.is_playing():
                await asyncio.sleep(1)
            await voiceClient.disconnect()
            os.remove(path)


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
