import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('laozibot.db') 
cursor = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS users (userid INTEGER PRIMARY KEY, username TEXT, admin BOOLEAN)')
if cursor.execute('SELECT * FROM users WHERE userid = 197139543135092736').fetchone() is None:
    cursor.execute('INSERT INTO users (userid, username, admin) VALUES (197139543135092736, "laozi", 1)')
conn.commit()

async def check_admin(ctx):
    cursor.execute("SELECT * FROM users WHERE userid = ?", (ctx.author.id,))
    row = cursor.fetchone()
    if row is None or row[2] == 0:
        embed = discord.Embed(title="You are not an admin", color=discord.Color.blue())
        await ctx.send(embed=embed)
        return False
    else:
        return True

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        if reaction.emoji == "❌":
            server = int(reaction.message.embeds[0].description.strip(" React with ❌ to leave"))
            server = self.bot.get_guild(server)
            await server.leave()

    @commands.command(name="servers", help="Show all servers")
    async def servers(self, ctx):
        if ctx.author == self.bot.user or not await check_admin(ctx):
            return
        for guild in self.bot.guilds:
            embed = discord.Embed(title=guild.name, description=f"{guild.id} React with ❌ to leave", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="users", help="Show all users")
    async def users(self, ctx):
        if ctx.author == self.bot.user or not await check_admin(ctx):
            return

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if len(rows) == 0:
            embed = discord.Embed(title="No users found", color=discord.Color.blue())
            await ctx.send(embed=embed)
            return
        for row in rows:
            embed = discord.Embed(title=row[0], description=row[1], color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="adduser", help="Add a user")
    async def adduser(self, ctx):
        if ctx.author == self.bot.user or not await check_admin(ctx):
            return
        else:
            message = ctx.message.content.removeprefix("!adduser ")
            user = self.bot.get_user(int(message))
            if user is None:
                embed = discord.Embed(title="User not found", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            if cursor.execute("SELECT * FROM users WHERE userid = ?", (user.id,)).fetchone() is not None:
                embed = discord.Embed(title="User already exists", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            cursor.execute("INSERT INTO users (userid, username, admin) VALUES (?, ?, ?)", (user.id, user.name, 0,))
            conn.commit()
            embed = discord.Embed(title=f"User {user.name} added", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="removeuser", help="Remove a user")
    async def removeuser(self, ctx):
        if ctx.author == self.bot.user or not await check_admin(ctx):
            return
        else:
            message = ctx.message.content.removeprefix("!removeuser ")
            user = self.bot.get_user(int(message))
            if user is None:
                embed = discord.Embed(title="User not found", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            if cursor.execute("SELECT * FROM users WHERE userid = ?", (user.id,)).fetchone() is None:
                embed = discord.Embed(title="User not found", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            cursor.execute("DELETE FROM users WHERE userid = ?", (user.id,))
            conn.commit()
            embed = discord.Embed(title=f"User {user.name} removed", color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
