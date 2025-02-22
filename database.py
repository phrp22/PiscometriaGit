import streamlit as st
from supabase import create_client

# Configuração do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def criar_usuario(email, senha):
    """ Cria um usuário no Supabase Authentication """
    response = supabase.auth.sign_up({
        "email": email,
        "password": senha
    })
    return response

def login_usuario(email, senha):
    """ Faz login no Supabase Authentication e retorna o usuário """
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": senha
    })
    return response

def get_user_by_id(user_id):
    """ Obtém o tipo de usuário baseado no ID """
    response = supabase.table("users").select("user_type").eq("id", user_id).execute()
    if response.data:
        return response.data[0]
    return {"user_type": "Paciente"}  # Retorna "Paciente" por padrão se não encontrar

def insert_paciente(profissional_id, paciente):
    """ Insere um novo paciente no banco de dados """
    if not profissional_id:
        raise ValueError("Erro: Profissional não encontrado!")

    response = supabase.table("pacientes").insert({
        "profissional": profissional_id,  # Agora usa o UUID correto
        "paciente": paciente
    }).execute()
    return response
