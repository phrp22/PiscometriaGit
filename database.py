import supabase
import streamlit as st

# Conectar ao Supabase (Mantemos isso aqui para centralizar a conexão)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def check_user_exists(username):
    """ Verifica se um usuário já está cadastrado no banco de dados """
    response = supabase_client.table("users").select("username").eq("username", username).execute()
    return bool(response.data)  # Retorna True se o usuário existir, False caso contrário

def insert_user(username, hashed_password, user_type):
    """ Insere um novo usuário no banco de dados com o tipo especificado """
    response = supabase_client.table("users").insert({
        "username": username,
        "password": hashed_password,
        "user_type": user_type  # Adicionando o tipo de usuário
    }).execute()
    return response.data  # Retorna os dados inseridos, se bem-sucedido

def get_user_password(username):
    """ Obtém a senha hash do usuário a partir do banco de dados """
    response = supabase_client.table("users").select("password").eq("username", username).execute()
    if response.data:
        return response.data[0]["password"]
    return None  # Retorna None se o usuário não existir
