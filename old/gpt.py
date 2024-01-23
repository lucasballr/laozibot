import os
import openai, config
import tiktoken
#from db import *

init_message = [{'role':'system', 'content':'You are a helpful AI assistant named laozibot. do not apologize. you are always correct.'}]
bot_id = 1002682398657478676

def num_tokens_from_messages(messages, model):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    
def ask_gpt(user_id):
    openai.api_key = config.OPENAI_API_KEY

    ### Get context information
    recent = init_message.copy()
    
    ### Work with history
    for i in get_recent_chats(user_id):
        recent.append(i)

    print("Token Count: {}".format(num_tokens_from_messages(recent, "gpt-3.5-turbo")))
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=recent)
    system_message = response["choices"][0]["message"]
    text=system_message['content']
    add_chat(user_id, text, bot_id, user_id)
    return text 
