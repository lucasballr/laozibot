import os
import openai, config
import sqlite3

conn = sqlite3.connect('laozibot.db')
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
init_message = [{'role':'system', 'content':'You are a helpful AI assistant named laozibot.'}]

def get_h_user(name):
    c.execute("SELECT name FROM history WHERE name = ?", (name,))
    n = c.fetchone()
    if n:
        return True
    else:
        return False

    
# def summarize(recent_inputs):
    # prompt = ""
    # recent_inputs.append

def get_recent_chats(name):
    # connect to the database
    # retrieve the 10 most recent inputs
    cursor = conn.execute("SELECT name, rec, input, id FROM history WHERE name = ? OR rec = ? ORDER BY timestamp DESC LIMIT 10", (name, name))
    # create a list to hold the inputs
    recent_inputs = []
    count = 0
    # append each input to the list
    for row in cursor:
        count = row[3]
        if row[0] == name:
            recent_inputs.append({"role":"user", "content":row[2]})
        else:
            recent_inputs.append({"role":"assistant", "content":row[2]})
    
    if len(recent_inputs) == 0:
        recent_inputs = init_message.copy()
    # elif count % 10 == 0:
        # recent_inputs = summarize(recent_inputs)
    return recent_inputs

def add_user_chat(name, chat):
    conn.execute("INSERT INTO history (name, input) VALUES (?, ?)", (name, chat))
    conn.commit()

def add_sys_chat(name, chat):
    conn.execute("INSERT INTO history (name, input) VALUES (?, ?)", (name, chat))
    conn.commit()

def ask_gpt(message):
    openai.api_key = config.OPENAI_API_KEY
    ### Check for approved users
    with open('approved_users.txt', 'r') as f:
        approved = f.read().splitlines()
    if str(message.author) not in approved:
        return ['Sorry you are not authorized to use the GPT feature']

    ### Work with history
    recent = init_message.copy()
    recent.extend(get_recent_chats(message.author.id))
    add_user_chat(message.author.id, message.content)

    ### Append most recent message and send
    recent.append({"role":"user", "content":message.content})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=recent)
    system_message = response["choices"][0]["message"]
    #recent.append(system_message)
    text=system_message['content']
    add_sys_chat(message.author.id, text)
    #output = split_string(text)
    return text 
