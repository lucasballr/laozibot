import discord
from discord.ext import commands
import yt_dlp

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play", help="Play something from YouTube")
    async def todo(self, ctx):
        if ctx.author == self.bot.user:
            return
        else:
            message = ctx.message.content.removeprefix("!play ")
            FFMPEG_OPTIONS = {
                'before_options':
                '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
                'options': '-vn'
            }

            embed = discord.Embed(title="Playing", color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))
