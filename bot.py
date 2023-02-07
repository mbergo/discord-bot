import discord
from discord.ext import commands
import openai
import requests
import json
import re
import sys

# Get the Discord bot token and GPT-3 API key from the openai_secret_manager
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: python3 bot.py <discord_token> <openai_api_key> <whatsapp_token> <github_token> <azure_token>")
    exit(0)

discord_token = sys.argv[1]
openai_key = sys.argv[2]
whatsapp_token = sys.argv[3]
github_token = sys.argv[4]
azure_token = sys.argv[5]


bot = commands.Bot(command_prefix='/', description="GPT-3 Discord Bot", intents=discord.Intents.all())

#
# using predy instead of talk in testing
#
@bot.command()
async def AI(ctx, *, message):
    # Use the GPT-3 API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}\n",
        max_tokens=2048,
        n = 1,
        stop=None,
        temperature=0.7,
        api_key = openai_key
    )

    # Send the response to the Discord channel
    await ctx.send(response.choices[0].text)


#
# create discord channel
#
@bot.command()
async def AI_criar_canal(room_id, channel_name, discord_token):
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
        
#        
# Send whatsapp msg        
#        
@bot.command()
async def AI_whatsapp(ctx, to, message):
    # Replace YOUR_AUTH_KEY with your WhatsApp Business API authorization key
    auth_key = whatsapp_token
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
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
#
# create groups
#
@bot.command()
async def AI_criar_grupo(ctx, team_name, *participants):
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

#
# Add job role
#
@bot.command()
async def predy_adicionar_cargo(ctx, member: discord.Member, job_title: str, color: discord.Color):
    guild = ctx.guild
    job_title = job_title.capitalize()
    
    # Check if the job title role exists, and create it if it doesn't
    role = discord.utils.get(guild.roles, name=job_title)
    if role is None:
        role = await guild.create_role(name=job_title, color=color)
    
    # Add the role to the member
    await member.add_roles(role)
    
    await ctx.send(f"{member.mention} was assigned the role {role.name} with color {role.color}.")

@bot.command()
async def AI_scan_issues(ctx, repo, github_token, bot_cmd):
    headers = {
        "Authorization": "Token " + github_token,
        "Accept": "application/vnd.github+json"
    }

    # Get all open issues in the repository
    url = f"https://api.github.com/repos/{repo}/issues?state=open"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Failed to retrieve issues from repository")
        return

    issues = json.loads(response.text)
    for issue in issues:
        # Check if the issue has any tags in the body
        tags = re.findall(r"/<(.*?)>", issue["body"])
        if tags:
            # Add labels to the issue based on the tags found
            for tag in tags:
                label_url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/labels"
                data = json.dumps([tag])
                requests.post(label_url, headers=headers, data=data)

        # Check if the issue has a bot command in the body
        bot_cmd = re.search(r"/bot (.*)", issue["body"])
        if bot_cmd:
            # Trigger the bot command and reply to the issue
            question = bot_cmd.group(1)
            response = requests.post("https://api.openai.com/v1/engines/davinci-002/jobs",
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps({"prompt": question, "max_tokens": 1024}),
                                     auth=(openai_key, ))
            await ctx.send(f"```{response.text}```")

            if response.status_code == 200:
                reply = response.json()["choices"][0]["text"].strip()
                comment_url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/comments"

        await ctx.send(f"===> {reply} posted to {comment_url}") 

            

@bot.command
async def AI_get_commits(ctx, branch_name, azure_token):
    headers = {
        "Authorization": "Bearer " + azure_token,
        "Accept": "application/json"
    }
    org_name = "predify"
    repo_name = "PriceGO"
    url = f"https://dev.azure.com/{org_name}/{repo_name}/_apis/git/repositories/{repo_name}/commits?api-version=6.1&$top=10&branch={branch_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = json.loads(response.text) 
        for commit in commits["value"]["comment"]:
            await ctx.send(f"{commit}")
    else:
        await ctx.send(f"Erro ao obter commits: {response.text}")



bot.run(discord_token)
