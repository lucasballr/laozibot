#! /usr/bin/env python3

import discord
from discord.ext import commands
# from gpt import ask_gpt, clear_history, show_history
import config
import paramiko
import os
import asyncio

os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

# Set up Discord stuff
discord_api_key = config.DISCORD_API_KEY
bot_id = 1002682398657478676

# Define bot's intents
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent

# Create a new instance of the bot client
bot = commands.Bot(command_prefix='!', intents=intents)

async def setup():
    for filename in os.listdir("./ext"):
        if filename.endswith(".py"):
            # Cut off the .py from the file name
            await bot.load_extension(f"ext.{filename[:-3]}")

asyncio.get_event_loop().run_until_complete(setup())
bot.run(discord_api_key)
