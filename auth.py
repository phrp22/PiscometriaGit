from supabase import create_client
import streamlit as st

# Configuração do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(email, password, user_type):
    """ Registra um novo usuário no Supabase Authentication """
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    if "user" in response:
        # Adicionamos o usuário na tabela `users` com o user_type definido
        supabase.table("users").insert({
            "id": response["user"]["id"],  # O Supabase gera um UUID automaticamente
            "email": email,
            "user_type": user_type
        }).execute()
    
    return response

def authenticate_user(email, password):
    """ Faz login no Supabase Authentication """
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    return response
