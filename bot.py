import discord
from discord.ext import commands
import openai

# Get the Discord bot token and GPT-2 API key from the openai_secret_manager
discord_token = "sys.argv[1]"
bot = commands.Bot(command_prefix='#', description="GPT-2 Discord Bot", intents=discord.Intents.all())

@bot.command()
async def talk(ctx, *, message):
    # Use the GPT-2 API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{message}\n",
        max_tokens=1024,
        n = 1,
        stop=None,
        temperature=0.5,
        api_key = "sys.argv[2]"
    )

    # Send the response to the Discord channel
    await ctx.send(response.choices[0].text)

bot.run(discord_token)
