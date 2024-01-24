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
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                ctx.send("You need to be in a channel first")
                return
            
            if ctx.voice_client is None:
                await voice_channel.connect()

            if ctx.voice_client.is_playing():
                await ctx.send("something is currently playing...")
                return
            
            FFMPEG_OPTIONS = {
                'before_options':
                '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
                'options': '-vn'
            }
            YDL_OPTIONS = { 
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            }
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(message, download=False)
                url2 = info['url']
                print(url2)
                source = discord.FFmpegPCMAudio(url2)
                vc = ctx.voice_client
                vc.play(source)

            embed = discord.Embed(title="Playing", color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))
