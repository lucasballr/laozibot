import os
import openai, config
import sqlite3
import tiktoken

conn = sqlite3.connect('laozidb.db')
conn.execute("""CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                rec TEXT,
                input TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

conn.execute("""CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                input TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

c = conn.cursor()
init_message = [{'role':'system', 'content':'You are a helpful AI assistant named laozibot. do not apologize. you are always correct.'}]

def get_h_user(c, conn, name):
    c.execute("SELECT name FROM history WHERE name = ?", (name,))
    n = c.fetchone()
    if n:
        return True
    else:
        return False

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
    
def get_recent_chats(c, conn, name):
    # connect to the database
    # retrieve the 10 most recent inputs
    cursor = conn.execute("SELECT name, rec, input, id FROM history WHERE name = ? OR rec = ? ORDER BY timestamp DESC LIMIT 10", (name,name))
    # create a list to hold the inputs
    recent_inputs = []
    # append each input to the list
    for row in cursor:
        count = row[3]
        if row[0] == str(name):
            recent_inputs.insert(0, {"role":"user", "content":row[2]})
        else:
            recent_inputs.insert(0, {"role":"assistant", "content":row[2]})
    
    return recent_inputs

def add_to_db(c, conn, name, rec, chat):
    #print("Adding chat to db. Name: {}, Rec: {}, Content: {}".format(name, rec, chat))
    conn.execute("INSERT INTO history (name, rec, input) VALUES (?, ?, ?)", (name, rec, chat))
    conn.commit()

def ask_gpt(message, weather):
    conn = sqlite3.connect('laozidb.db')
    c = conn.cursor()
    openai.api_key = config.OPENAI_API_KEY
    ### Check for approved users
    with open('approved_users.txt', 'r') as f:
        approved = f.read().splitlines()
    if str(message.author) not in approved:
        return 'Sorry you are not authorized to use the GPT feature'

    ### Get context information
    recent = init_message.copy()
    recent.append({'role':'system', 'content':'The following data is up-to-date information about the weather at the user\'s location. Do not make guesses about weather information.: {}.'.format(weather)})

    ### Work with history
    for i in get_recent_chats(c, conn, message.author.id):
        recent.append(i)
    add_to_db(c, conn, message.author.id, 'assistant', message.content)

    ### Append most recent message and send
    recent.append({"role":"user", "content":message.content})
    ### Uncomment this for debugging the program.
    #for i in recent:
        #print(i)
    print("Token Count: {}".format(num_tokens_from_messages(recent, "gpt-3.5-turbo")))
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=recent)
    system_message = response["choices"][0]["message"]
    #print(system_message)
    text=system_message['content']
    add_to_db(c, conn, 'assistant', message.author.id, text)
    return text 
