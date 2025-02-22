import streamlit as st
from supabase import create_client

# Configuração do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def criar_usuario(email, senha):
    """ Cria um usuário no Supabase Authentication """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": senha
        })
        return response
    except Exception as e:
        return {"error": str(e)}

def login_usuario(email, senha):
    """ Faz login no Supabase Authentication e retorna o usuário """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })
        return response
    except Exception as e:
        return {"error": str(e)}

def get_user_by_id(user_id):
    """ Obtém o tipo de usuário baseado no ID """
    try:
        response = supabase.table("users").select("user_type").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return {"user_type": "Paciente"}  # Retorna "Paciente" por padrão se não encontrar
    except Exception as e:
        return {"error": str(e)}

def insert_paciente(profissional_id, paciente):
    """ Insere um novo paciente no banco de dados """
    if not profissional_id:
        raise ValueError("Erro: Profissional não encontrado!")

    try:
        response = supabase.table("pacientes").insert({
            "profissional": profissional_id,  # Agora usa o UUID correto
            "paciente": paciente
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def register_user(username, password, user_type):
    """ Registra um novo usuário no Supabase Authentication e na tabela `users` """
    try:
        response = supabase.auth.sign_up({
            "email": username,  # O Supabase Authentication usa e-mail para login
            "password": password
        })

        if "user" in response:
            user_id = response["user"]["id"]  # Pega o UUID gerado pelo Supabase

            # Insere os dados do usuário na tabela `users`
            supabase.table("users").insert({
                "id": user_id,
                "username": username,  # Agora usamos `username`
                "user_type": user_type  # O tipo de usuário (Profissional/Paciente)
            }).execute()
        
        return response
    except Exception as e:
        return {"error": str(e)}
