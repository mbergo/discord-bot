import discord
from discord.ext import commands
import openai
import requests

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
@bot.command()
def predy_criar_canal(room_id, channel_name, discord_token):
    headers = {
        "Authorization": f"Bot {discord_token}",
        "User-Agent": "MyBot/0.0.1",
        "Content-Type": "application/json",
    }

    payload = {
        "name": channel_name,
        "type": 0, # 0 for text channel, 2 for voice channel
    }

    url = f"https://discord.com/api/guilds/{room_id}/channels"

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f"Successfully created channel '{channel_name}'")
    else:
        print(f"Failed to create channel. Response: {response.text}")

@bot.command()
async def predy_whatsapp(ctx, to, message):
    # Replace YOUR_AUTH_KEY with your WhatsApp Business API authorization key
    auth_key = "YOUR_AUTH_KEY"
    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Content-Type": "application/json"
    }
    # Replace YOUR_WHATSAPP_NUMBER with your WhatsApp Business number
    from_number = "YOUR_WHATSAPP_NUMBER"
    data = {
        "from": from_number,
        "to": to,
        "message": message
    }
    response = requests.post("https://api.whatsapp.com/v1/messages", headers=headers, json=data)
    if response.status_code == 200:
        await ctx.send(f"Mensagem enviada com sucesso para {to}.")
    else:
        await ctx.send(f"Erro ao enviar mensagem para {to}: {response.text}")


bot.run(discord_token)
