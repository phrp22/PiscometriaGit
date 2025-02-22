import supabase
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def check_user_exists(username):
    response = supabase_client.table("users").select("username").eq("username", username).execute()
    return bool(response.data)

def insert_user(username, hashed_password, user_type):
    response = supabase_client.table("users").insert({
        "username": username,
        "password": hashed_password,
        "user_type": user_type
    }).execute()
    return response

def get_user_credentials(username):
    response = supabase_client.table("users").select("password", "user_type").eq("username", username).execute()
    if response.data:
        return response.data[0]
    return None