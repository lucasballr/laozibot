#! /usr/bin/env python3

import discord
from discord.ext import commands
from gpt import ask_gpt
#from dotenv import load_dotenv
import config
#from db import *
#from helpers import *
import paramiko

#load_dotenv()
#discord_api_key: str = os.getenv("DISCORD_API_KEY")
discord_api_key = config.DISCORD_API_KEY
bot_id = 1002682398657478676

# Define  bot's intents
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent

ssh = paramiko.SSHClient()
k = paramiko.Ed25519Key.from_private_key_file('./pz')
# OR k = paramiko.DSSKey.from_private_key_file(keyfilename)

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
pz_command = "sudo systemctl restart pz.service"
authorized_users = [197139543135092736, 197140256124960768, 263223388577857536, 1089100243120963584]
# Create a new instance of the bot client
client = commands.Bot(command_prefix='!', intents=intents)

@client.command(name="rpz") 
async def rpz(ctx):
    if ctx.author == client.user:
        return
    elif ctx.author.id in authorized_users:
        print("Restarting pz server")
        ssh.connect(hostname='192.168.1.185', username="pzuser", pkey=k)
        stdin, stdout, stderr = ssh.exec_command(pz_command)
    else:
        return

client.run(discord_api_key)
