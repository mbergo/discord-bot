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
async def predy_criar_canal(ctx, room, channel, category, channel_type):
    guild = ctx.guild
    category = category.lower()
    channel_type = channel_type.lower()

    existing_category = discord.utils.get(guild.categories, name=category)
    if not existing_category:
        existing_category = await guild.create_category(category)

    existing_channel = discord.utils.get(guild.channels, name=channel)
    if not existing_channel:
        if channel_type == "text":
            new_channel = await guild.create_text_channel(channel, category=existing_category)
        elif channel_type == "voice":
            new_channel = await guild.create_voice_channel(channel, category=existing_category)
        else:
            await ctx.send(f"Tipo de canal inválido. Escolha entre 'text' ou 'voice'.")
            return

        await new_channel.send(f"Canal {channel_type} criado na sala {room}, na categoria {category}.")
    else:
        await ctx.send(f"O canal {channel} já existe na sala {room}.")


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
