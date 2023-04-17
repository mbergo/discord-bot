import openai
import asyncio
import requests
import discord
from discord.ext import commands
import json
import re
import sys
import time

# Get the Discord bot token and AI4d API key from the openai_secret_manager
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: python3 bot.py <discord_token> <openai_api_key> <whatsapp_token> <github_token> <azure_token>")
    exit(0)

discord_token = sys.argv[1]
openai_key = sys.argv[2]

# Initialize the Discord bot and a dictionary to store conversation history
bot = commands.Bot(command_prefix='/', description="AI4D Bot", intents=discord.Intents.all())
conversation_history = {}


#
# using predy instead of talk in testing
#
@bot.command()
async def ai4d(ctx, *, message):
    user_id = ctx.message.author.id
    channel_id = ctx.message.channel.id
    user_channel_key = f"{user_id}-{channel_id}"

    # Add the user message to the conversation history
    if user_channel_key not in conversation_history:
        conversation_history[user_channel_key] = []
    conversation_history[user_channel_key].append(f"{message}")

    # Concatenate the conversation history for the AI4d API prompt
    prompt = "\n".join(conversation_history[user_channel_key]) + "\n"

    # Use the AI4d API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n = 1,
        stop=None,
        temperature=0.7,
        api_key = openai_key
    )

    # Add the AI4d response to the conversation history
    conversation_history[user_channel_key].append(f"{response.choices[0].text.strip()}")

    # Send the response to the Discord channel
    await ctx.send("```" + response.choices[0].text.strip() + "```")

while True:
    try:
        bot.run(discord_token, reconnect=True)
    except Exception as APIConnectionError:
        print("Erro ao conectar ao Discord. Tentando novamente em 5 segundos...")
        time.sleep(5)
        bot.run(discord_token, reconnect=True)


