import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('laozibot.db') 
cursor = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS todo (userid INTEGER, todo TEXT)')

class Note(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        if reaction.emoji == "✅":
            cursor.execute("DELETE FROM todo WHERE rowid = ?", (reaction.message.embeds[0].title,))
            conn.commit()

    @commands.command(name="note", help="Add a note")
    async def note(self, ctx):
        if ctx.author == self.bot.user:
            return

    @commands.command(name="notes", help="Show all notes")
    async def notes(self, ctx):
        if ctx.author == self.bot.user:
            return

    @commands.command(name="todo", help="Add a todo")
    async def todo(self, ctx):
        if ctx.author == self.bot.user:
            return
        else:
            message = ctx.message.content.removeprefix("!todo ")
            cursor.execute("INSERT INTO todo (userid, todo) VALUES (?, ?)", (ctx.author.id, message,))
            conn.commit()
            embed = discord.Embed(title="Todo added", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="todos", help="Show all todos")
    async def todos(self, ctx):
        if ctx.author == self.bot.user:
            return
        cursor.execute("SELECT rowid, todo FROM todo WHERE userid = ?", (ctx.author.id,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            embed = discord.Embed(title="No todos found", color=discord.Color.blue())
            await ctx.send(embed=embed)
            return
        for row in rows:
            embed = discord.Embed(title=row[0], description=row[1], color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Note(bot))
