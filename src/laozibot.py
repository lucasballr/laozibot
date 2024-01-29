#! /usr/bin/env python3

import discord
from discord.ext import commands
from discord import app_commands
# from gpt import ask_gpt, clear_history, show_history
import config
import paramiko
import os
import asyncio

os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

# Set up Discord stuff
discord_api_key = config.DISCORD_API_KEY
bot_id = 1002682398657478676
guild_ids = [197140763690270720]

# Create a new instance of the bot client
#bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

class LaozibotClient(discord.Client):
    def __init__(self, intents):
        
        self.intents = intents
        tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        tree.copy_global_to(guild=discord.Object(id=guild_ids[0])) # Optional if you don't want global?
        await tree.sync(guild=discord.Object(id=guild_ids[0]))

client = LaozibotClient(intents=discord.Intents.all())
# client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# tree = app_commands.CommandTree(client)
tree = client.tree




# .command()
# async def sync(ctx):
#     print("sync command")
#     if ctx.author.id == 197139543135092736:
#         await tree.sync(guild=discord.Object(id=guild_ids[0]))
#         await ctx.send('Command tree synced.')
#     else:
#         await ctx.send('You must be the owner to use this command!')

# @app_commands.command(name = "sync", description="Syncs the bot commands", guild=discord.Object(id=guild_ids[0]))
# async def sync(interaction: discord.Interaction):
#     if interaction.user.id == 197139543135092736:
#         #client.tree.copy_global_to(guild=discord.Object(id=guild_ids[0]))
#         await client.tree.sync(guild=discord.Object(id=guild_ids[0]))
#         await interaction.response.send_message('Command tree synced.')
#     else:
#         await interaction.response.send('You must be the owner to use this command!')

@app_commands.command(name = "ping", description="Pings the bot!")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in guild_ids])
async def ping(inter: discord.Interaction) -> None:
    await inter.response.send_message(f"> Pong! {round(client.latency * 1000)}ms")

@app_commands.command(name = "help", description="Displays help message")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in guild_ids])
async def help(inter: discord.Interaction) -> None:
    await inter.response.send_message("This is a test help message")

tree.add_command(ping)
tree.add_command(help)
# tree.add_command(sync)

### If I want to add a message to the command:
# @bot.tree.command(name="ping", description="Pings the bot")
# @app_commands.describe()
# async def _ping(interaction: discord.Interaction, message: str) -> None:
#     await interaction.response.send_message(f"Pong! ({bot.latency*1000}ms)")



# @bot.slash(name='ping', guild_ids=guild_ids)  # Replace GUILD_ID with your guild ID
# async def _ping(ctx):
#     await ctx.respond(f"Pong! ({client.latency*1000}ms)")


'''
bot = commands.Bot(command_prefix='!', intents=intents)

async def setup():
    for filename in os.listdir("./ext"):
        if filename.endswith(".py"):
            # Cut off the .py from the file name
            await bot.load_extension(f"ext.{filename[:-3]}")

asyncio.get_event_loop().run_until_complete(setup())
'''



# async def setup_hook() -> None:  # This function is automatically called before the bot starts
#     client.tree.copy_global_to(guild=discord.Object(id=guild_ids[0]))
#     await client.tree.sync(guild=discord.Object(id=guild_ids[0]))
# #
# @client.event
# async def on_ready() -> None:  # This event is called when the bot is ready
#     await client.tree.sync(guild=discord.Object(id=guild_ids[0]))
#     print(f"Logged in as {client.user}")

# client.setup_hook = setup_hook

client.run(discord_api_key)
