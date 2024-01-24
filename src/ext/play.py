import discord
from discord.ext import commands
import youtube_dl

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play", help="Play something from YouTube")
    async def todo(self, ctx):
        if ctx.author == self.bot.user:
            return
        else:
            message = ctx.message.content.removeprefix("!play ")

            embed = discord.Embed(title="Playing", color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))
