import discord
from discord.ext import commands
import openai
import requests

# Get the Discord bot token and GPT-2 API key from the openai_secret_manager
discord_token = "sys.argv[1]"
bot = commands.Bot(command_prefix='/', description="GPT-2 Discord Bot", intents=discord.Intents.all())


# using predy instead of talk in testing
@bot.command()
async def talk(ctx, *, message):
    # Use the GPT-2 API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}\n",
        max_tokens=2x1024,
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
    from_number = "+55000000000"
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

# Criar canais
@bot.command()
async def predy_criar_grupo(ctx, team_name, *participants):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name=team_name)
    if not existing_role:
        new_role = await guild.create_role(name=team_name)
        await new_role.edit(mentionable=True)
    else:
        new_role = existing_role
    participants = [p.strip() for p in participants]
    member_objects = [discord.utils.get(guild.members, name=p) for p in participants]
    member_objects = [m for m in member_objects if m is not None]
    if not member_objects:
        await ctx.send(f"Nenhum participante foi encontrado.")
    else:
        for member in member_objects:
            await member.add_roles(new_role)
        await ctx.send(f"Grupo {team_name} criado com os seguintes participantes: {', '.join([m.name for m in member_objects])}.")

# Adicionar cargo
@bot.command()
async def predy_adicionar_cargo(ctx, member: discord.Member, job_title: str):
    guild = ctx.guild
    job_title = job_title.capitalize()
    
    # Check if the job title role exists, and create it if it doesn't
    role = discord.utils.get(guild.roles, name=job_title)
    if role is None:
        role = await guild.create_role(name=job_title)
    
    # Add the role to the member
    await member.add_roles(role)
    
    await ctx.send(f"{member.mention} was assigned the role {role.name}.")


bot.run(discord_token)
