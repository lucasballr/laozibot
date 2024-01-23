import os
import openai
import config
import tiktoken
from discord.ext import commands
import discord

init_message = [{'role':'system', 'content':'You are a helpful AI assistant named laozibot. do not apologize. you are always correct. Respond to every message in under 2000 characters'}]
bot_id = 1002682398657478676
authorized_gpt = [197139543135092736]
user_dict = {}

def num_tokens_from_messages(messages, model):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-4":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens

def clear_history(user_id):
    if user_id not in user_dict:
        return "No chat history to clear"
    else:
        del user_dict[user_id]
        return "Chat history cleared"

def show_history(user_id):
    if user_id not in user_dict:
        return ["No chat history to show"]
    else:
        return user_dict[user_id]
    
def ask_gpt(user_id, message):
    openai.api_key = config.OPENAI_API_KEY
    client = openai.Client()

    ### Get context information
    recent = init_message.copy()
    
    ### Work with history
    if user_id not in user_dict:
        user_dict[user_id] = []
    for i in user_dict[user_id]:
        recent.append(i)
    recent.append({"role":"user", "content":message})

    ### Get response
    # print("Token Count: {}".format(num_tokens_from_messages(recent, "gpt-4")))
    response = client.chat.completions.create(model="gpt-4", messages=recent)
    sys_message = response.choices[0].message
    print(f"Laozibot: {sys_message.content}")
    system_message = {'role':sys_message.role, 'content':sys_message.content}
    text=system_message['content']

    ### Update history
    recent.append(system_message)
    if len(recent) > 10:
        recent = recent[-10:]
    user_dict[user_id] = recent[1:]

    return text

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask LaoziBot a question")
    async def ask(self, ctx):
        if ctx.author == self.bot.user:
            return
        elif ctx.author.id in authorized_gpt:
            message = ctx.message.content.strip("!ask ")
            print(f"{ctx.author}: {message}")
            await ctx.send(ask_gpt(ctx.author.id, message))
        else:
            return

    @commands.command(name="clear", help="Clear LaoziBot's chat history")
    async def clear(self, ctx):
        if ctx.author == self.bot.user:
            return
        elif ctx.author.id in authorized_gpt:
            print(f"Clearing chat history for {ctx.author.name}")
            embed = discord.Embed(title=clear_history(ctx.author.id), color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            return

    @commands.command(name="hist", help="Show LaoziBot's chat history")
    async def hist(self, ctx):
        if ctx.author == self.bot.user:
            return
        elif ctx.author.id in authorized_gpt:
            history = show_history(ctx.author.id)
            for i in history:
                await ctx.send(i)
        else:
            return

async def setup(bot):
    await bot.add_cog(Gpt(bot))
