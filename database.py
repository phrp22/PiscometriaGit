import supabase
import streamlit as st

# Conectar ao Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_password(username):
    """ Obtém a senha do usuário armazenada no banco de dados. """
    response = supabase_client.table("users").select("password").eq("username", username).execute()
    if response.data:
        return response.data[0]["password"]
    return None

def insert_user(username, hashed_password):
    """ Insere um novo usuário no banco de dados. """
    response = supabase_client.table("users").insert({
        "username": username,
        "password": hashed_password
    }).execute()
    return response