# Discord Secure Shell
A Discord bot that functions as an ssh client! You can add this bot to any server you want and impress your friends with your amazing hacker skills!

Runs on linux and MacOS, not tested on anything else

## Prerequisites
First, you need a Discord server to add the ssh client to. Use the name of the server as the `DISCORD_GUILD` in your `.env` file (described below)

You'll also need to create a bot using your Discord developer account. Follow [this tutorial](https://realpython.com/how-to-make-a-discord-bot-python/) up until the part where it says "How to Make a Discord Bot in Python" (that's what this is!) Copy your bot token (Bot tab -> Token) and paste it in for `DISCORD_TOKEN` in your `.env` file (described below)

## Installation
First, make sure all the requirements are installed:
```bash
python3 -m pip install -r requirements.txt
```

Next, create a `.env` file.
Discord Secure Shell uses a `.env` file to keep track of api keys and stuff. Here's an example:
```bash
DISCORD_TOKEN=this_is_not_a_real_bot_token
DISCORD_GUILD='name of your server'
```

For instructions on how to obtain the various api keys and stuff, see the prerequisites section.

## Running
Run the bot using
```bash
python3 bot.py
```
