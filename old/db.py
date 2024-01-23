import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SECRET")
supabase: Client = create_client(url, key)


def add_user(user, user_id):
    res = supabase.table('users').select("*").eq("discord_id", user_id).execute()
    if res.data:
        return "User already signed up"
    else:
        data, count = supabase.table('users').insert({"discord_username": user.name, "discord_id": user_id}).execute()
        return "User added"
        
def del_user(user_id):
    res = supabase.table('users').select("*").eq("discord_id", user_id).execute()
    if res.data:
        data, count = supabase.table('users').delete().eq("discord_id", user_id).execute()
        return "User deleted"
    else:
        return "User does not exist"

def make_admin(user_id):
    res = supabase.table('users').select("*").eq("discord_id", user_id).execute()
    if res.data:
        user = res.data[0]
        if user["is_admin"] == False:
            data, count = supabase.table('users').update({"is_admin": True}).eq("discord_id", user["discord_id"]).execute()
    
def remove_admin(user_id):
    res = supabase.table('users').select("*").eq("discord_id", user_id).execute()
    if res.data:
        user = res.data[0]
        if user["is_admin"] == True:
            data, count = supabase.table('users').update({"is_admin": False}).eq("discord_id", user["discord_id"]).execute()

def check_admin(user):
    res = supabase.table('users').select("*").eq("discord_id", user.id).execute()
    if res.data[0]["is_admin"]:
        return True
    else:
        return False

def check_user(user):
    res = supabase.table('users').select("*").eq("discord_id", user.id).execute()
    if res.data:
        return True
    else:
        return False

def get_recent_chats(user_id):
    res = supabase.table('history').select("sender, reciever, text").eq("user_id", user_id).order('created_at', desc=True).limit(10).execute()
    recent_inputs = []
    for row in res.data:
        if row['sender'] == user_id:
            recent_inputs.insert(0, {"role":"user", "content":row['text']})
        else:
            recent_inputs.insert(0, {"role":"assistant", "content":row['text']})
    return recent_inputs

def add_chat(user_id, text, sender, reciever):
    data, count = supabase.table('history').insert({"user_id": user_id, "sender": sender, "reciever": reciever, "text": text}).execute()
    
def clear_chats(user_id):
    data, count = supabase.table('history').delete().eq("user_id", user_id).execute()
