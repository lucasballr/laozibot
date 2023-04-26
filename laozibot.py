#! /usr/bin/env python

import discord
from discord.ext import commands
import os
import openai, config
import asyncio
import sqlite3
import re
from datetime import datetime, timedelta
import json
from w6 import get_user, get_weather, get_location, update_location, add_user
from gpt import ask_gpt

openai.api_key = config.OPENAI_API_KEY
discord_api_key = config.DISCORD_API_KEY

# Connect to the database
db_conn = sqlite3.connect('laozidb.db')
db_conn.execute('CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, remind_at INTEGER, content TEXT)')
db_conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, location TEXT)''')
command_list = ['!r', '!w']
init_message = [{'role':'system', 'content':'You are a helpful AI assistant named laozibot.'}]
reminders = {}
messages = init_message
users = {}
# Define your bot's intents
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent

# Create a new instance of the bot client
client = commands.Bot(command_prefix='!', intents=intents)

def extract_code(text):
    pattern = r'(```[\s\S]+?```)'  # Add capturing group with parentheses
    segments = re.split(pattern, text)
    return segments
    
def split_string(input_string):
    # check if the input string is larger than 2000 characters
    if '```' in input_string:
        input_string = extract_code(input_string)
    else:
        input_string = [input_string]
    new_strings = []
    for s in input_string:
        if len(s) > 2000:
            # split the input string into chunks of 2000 characters or less
            chunks = [input_string[i:i+1999] for i in range(0, len(s), 1999)]
            new_strings.extend(chunks)
        else:
            new_strings.append(s)
        # if the input string is less than or equal to 2000 characters, return it as is
    return new_strings

async def schedule_reminder(user, duration, content, reminder_id):
    # Wait until the reminder is due
    await asyncio.sleep(duration)

    # Send the reminder to the user
    await user.send(f'Reminder: {content}')

    # Delete the reminder from the database
    db_conn.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
    db_conn.commit()

    # Check for any remaining reminders that are due
    for row in db_conn.execute('SELECT * FROM reminders WHERE remind_at <= ?', (int(datetime.utcnow().timestamp()),)):
        user_id, remind_at, content, remaining_reminder_id = row
        user = await client.fetch_user(int(user_id))
        duration = max(remind_at - int(datetime.utcnow().timestamp()), 0)
        asyncio.ensure_future(schedule_reminder(user, duration, content, remaining_reminder_id))

def remind(message):
    # Parse the reminder duration and message content
    duration, content = message.content[10:].split(' ', 1)
    # Convert the duration (in minutes) to seconds
    if duration.endswith('s'):
        duration = int(duration[:-1])
    elif duration.endswith('m'):
        duration = int(duration[:-1]) * 60
    elif duration.endswith('h'):
        duration = int(duration[:-1]) * 60 * 60
    elif duration.endswith('d'):
        duration = int(duration[:-1]) * 60 * 60 * 24
    # Schedule the reminder
    remind_at = int(message.created_at.timestamp()) + duration
     # Store the reminder in the database and schedule it
    cursor = db_conn.cursor()
    cursor.execute('INSERT INTO reminders (user_id, remind_at, content) VALUES (?, ?, ?)', (str(message.author.id), remind_at, content))
    db_conn.commit()
    reminder_id = cursor.lastrowid
    cursor.close()
    asyncio.ensure_future(schedule_reminder(message.author, duration, content, reminder_id))

def weather(message):
    cmd = message.content.split(' ')
    user = message.author.id
    
    if len(cmd) == 1:
        if not get_user(db_conn, user):
            return "You're not registered, to register type '!w <location>'"
        elif not get_location(db_conn, user):
            return "You need to add a location for yourself '!w <location>'"
    elif len(cmd) > 1:
        location = cmd[1]
        if not get_user(db_conn, user):
            add_user(db_conn, user, location)
        else:
            update_location(db_conn, user, location)
    else:
        return "Invalid command"
    
    loc = get_location(db_conn, user)
    w = get_weather(loc)
    m = init_message.copy()
    p = "Here is some information about the weather in my area: "
    for i in w:
        p += i + " "
    p += "Based on this information, suggest how I should go about my day in 50 words or less"
    m.append({"role":"user", "content":p})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=m)
    sys_res = response["choices"][0]["message"]
    return sys_res['content']

def run_command(message):
    cmd = message.content.split(' ')[0]
    if cmd == '!r':
        remind(message)
        return "Reminder Set"
    elif cmd == '!w':
        return weather(message)
    else:
        return "Command Error. Idk how you got here."

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    # Remember the reminders
    for row in db_conn.execute('SELECT * FROM reminders WHERE remind_at > ?', (int(discord.utils.time_snowflake(datetime.utcnow() - timedelta(minutes=1))),)):
        user_id, remind_at, content = row[1:]
        user = await client.fetch_user(int(user_id))
        duration = max(remind_at - int(datetime.utcnow().timestamp()), 0)
        asyncio.ensure_future(schedule_reminder(user, duration, content, row[0]))

@client.event
async def on_message(message):
    print("{}: {}".format(message.author.name, message.content))
    if message.author == client.user:
        return

    # Check if message is in a DM or the message starts with !g
    if isinstance(message.channel, discord.DMChannel) or message.content.startswith('!g'):
        async with message.channel.typing():
            pass
        
        if message.content.split(' ')[0] in command_list:
            await message.channel.send(run_command(message))
        else:
            output = split_string(ask_gpt(message))
            for i in output:
                if i != "":
                    await message.channel.send(i)
    elif message.content.split(' ')[0] in command_list:
        run_command(message)

client.run(discord_api_key)
