import unittest
import bot
import discord
from discord.ext import commands
import io
import sys

class TestGPT2Talk(unittest.TestCase):

    def setUp(self):
        self.bot = bot.bot,sys.argv[1],sys.argv[2]
        self.gpt2_talk = self.bot.get_command("talk")
        self.test_channel = discord.Object(id='test_channel_id')
        self.test_server = discord.Object(id='test_server_id')
        self.test_author = discord.Object(id='test_author_id')
        self.test_message = discord.Object(channel=self.test_channel, author=self.test_author, server=self.test_server)

    def test_talk(self):
        # redirect stdout to capture bot's response
        sys.stdout = io.StringIO()
        # call the gpt2_talk command
        self.talk.callback(self.bot, self.test_message, "What is the meaning of life?")
        # check if the bot's response is not empty
        self.assertTrue(sys.stdout.getvalue().strip())

if __name__ == '__main__':
    unittest.main()

