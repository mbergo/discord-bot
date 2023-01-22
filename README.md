# Discord GPT-2 Bot
A Discord bot that uses GPT-2 to talk to people.

## How to use
Invite the bot to your Discord server by generating an invite link on the "OAuth2" page. Select the permissions you want the bot to have and generate the link. Have the server owner click on the link to add the bot to the server.

Once the bot is connected to the server, you can use the command prefix you set in the code to interact with the bot and use the `talk` command on any channel where the bot has access to.

To ask the bot a question, type in the following command in the channel:
```
#talk [your question]
```
## How to run
To run this bot, you need to have the discord bot token and the OpenAI API key. You can get them by creating an application and a bot on the Discord Developer Portal and a API key on the OpenAI portal.

You can also use the openai_secret_manager to handle your API keys.

Once you have the keys, you can run the script by running the following command:
`python3 bot.py`
Also, you can use the provided Dockerfile to build an image and run it using docker.

#### Requirements
Python 3.9
discord.py
openai
openai_secret_manager (if you want to handle the API keys using this library)
####Note
This bot's understanding of the question is based on the training data it was exposed to, and the bot can make mistakes on certain questions.
