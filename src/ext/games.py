import discord
from discord.ext import commands
import paramiko

ssh = paramiko.SSHClient()
k = paramiko.Ed25519Key.from_private_key_file('./pz')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Set up Projext Zomboid stuff
pz_command = "sudo systemctl restart pz.service"
authorized_users = [197139543135092736, 197140256124960768, 263223388577857536, 1089100243120963584]

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rpz", help="Restart Project Zomboid server")
    async def rpz(self, ctx):
        if ctx.author == self.bot.user:
            return
        elif ctx.author.id in authorized_users:
            print("Restarting pz server")
            ssh.connect(hostname='192.168.1.185', username="pzuser", pkey=k)
            stdin, stdout, stderr = ssh.exec_command(pz_command)
        else:
            return

async def setup(bot):
    await bot.add_cog(Games(bot))
