#! /usr/bin/env python3

import discord
from discord.ext import commands
from gpt import ask_gpt
from dotenv import load_dotenv
from db import *
from helpers import *

load_dotenv()
discord_api_key: str = os.getenv("DISCORD_API_KEY")
bot_id = 1002682398657478676

# Define  bot's intents
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent

# Create a new instance of the bot client
client = commands.Bot(command_prefix='!', intents=intents)

@client.command(name="remove_admin")
async def _remove_admin(ctx, *arg):
    if ctx.author == client.user:
        return
    if not check_admin(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You are not a registered admin", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if len(arg) < 1 or len(arg) > 1:
        embed = discord.Embed(title="Laozibot", description="Format: !remove_admin <user_id>", color=0xff0000)
        await ctx.send(embed=embed)
        return
    else:
        try:
            user_id = int(arg[0])
        except:
            return
        user = client.get_user(user_id)
        if user and check_user(user):
            remove_admin(user_id)
            embed = discord.Embed(title="Laozibot", description="User {} is no longer admin".format(user), color=0x00ff00)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Laozibot", description="User not found", color=0xff0000)
            await ctx.send(embed=embed)
            return

@client.command(name="make_admin")
async def _make_admin(ctx, *arg):
    if ctx.author == client.user:
        return
    if not check_admin(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You are not a registered admin", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if len(arg) < 1 or len(arg) > 1:
        embed = discord.Embed(title="Laozibot", description="Format: !make_admin <user_id>", color=0xff0000)
        await ctx.send(embed=embed)
        return
    else:
        try:
            user_id = int(arg[0])
        except:
            return
        user = client.get_user(user_id)
        if user and check_user(user):
            make_admin(user_id)
            embed = discord.Embed(title="Laozibot", description="User {} is now admin".format(user), color=0x00ff00)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Laozibot", description="User not found", color=0xff0000)
            await ctx.send(embed=embed)
            return

@client.command(name="add_user")
async def _add_user(ctx, *arg):
    if ctx.author == client.user:
        return
    if not check_admin(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You are not a registered admin", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if len(arg) < 1 or len(arg) > 1:
        embed = discord.Embed(title="Laozibot", description="Format: !add_user <user_id>", color=0xff0000)
        await ctx.send(embed=embed)
        return
    else:
        try:
            user_id = int(arg[0])
        except:
            return
        user = client.get_user(user_id)
        if user:
            add_user(user, user_id)
            embed = discord.Embed(title="Laozibot", description="User {} added".format(user), color=0x00ff00)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Laozibot", description="User not found", color=0xff0000)
            await ctx.send(embed=embed)
            return

@client.command(name="del_user")
async def _del_user(ctx, *arg):
    if ctx.author == client.user:
        return
    if not check_admin(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You are not a registered admin", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if len(arg) < 1 or len(arg) > 1:
        embed = discord.Embed(title="Laozibot", description="Format: !del_user <user_id>", color=0xff0000)
        await ctx.send(embed=embed)
        return
    else:
        try:
            user_id = int(arg[0])
        except:
            return
        user = client.get_user(user_id)
        if user and check_user(user):
            del_user(user_id)
            embed = discord.Embed(title="Laozibot", description="User {} removed".format(user), color=0x00ff00)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Laozibot", description="User not found", color=0xff0000)
            await ctx.send(embed=embed)
            return

@client.command(name="clear")
async def _clear(ctx):
    if ctx.author == client.user:
        return
    if not check_user(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You are not a registered user", color=0xff0000)
        await ctx.send(embed=embed)
        return
    clear_chats(ctx.author.id)
    embed = discord.Embed(title="Laozibot", description="Chat history cleared", color=0x00ff00)
    await ctx.send(embed=embed)

@client.command(name="g")
async def _g(ctx, *arg):
    if ctx.author == client.user:
        return
    if not check_user(ctx.author):
        embed = discord.Embed(title="Laozibot", description="You do not have permission for this", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if arg:
        ' '.join(arg)
    else:
        embed = discord.Embed(title="Laozibot", description="Format: !g <message>", color=0xff0000)
        await ctx.send(embed=embed)
    add_chat(ctx.author.id, arg, ctx.author.id, bot_id)
    async with message.channel.typing():
        response = ask_gpt(ctx.author.id)
    print("{}: {}".format(ctx.author.name, arg))
    print("Laozibot: {}".format(response))
    for i in split_string(response):
        await ctx.send(i)
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel) and not message.content.startswith("!"):
        if not check_user(message.author):
            embed = discord.Embed(title="Laozibot", description="You do not have permission for this", color=0xff0000)
            await message.channel.send(embed=embed)
            return
        add_chat(message.author.id, message.content, message.author.id, bot_id)
        async with message.channel.typing():
            response = ask_gpt(message.author.id)
        print("{}: {}".format(message.author.name, message.content))
        print("Laozibot: {}".format(response))
        for i in split_string(response):
            await message.channel.send(i)
    else:
        await client.process_commands(message)

client.run(discord_api_key)
