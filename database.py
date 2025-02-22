import supabase
import bcrypt
import streamlit as st

# Conectar ao Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password):
    """ Gera um hash seguro para a senha """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def cadastrar_paciente(profissional, paciente_username, paciente_password):
    """ Cadastra um novo paciente no banco de dados """
    
    # Verificar se o paciente já existe
    response = supabase_client.table("users").select("username").eq("username", paciente_username).execute()
    if response.data:
        return {"success": False, "message": "Este paciente já está cadastrado."}

    # Criar conta do paciente no banco 'users'
    hashed_password = hash_password(paciente_password)
    user_response = supabase_client.table("users").insert({
        "username": paciente_username,
        "password": hashed_password,
        "user_type": "Paciente"
    }).execute()

    if user_response.error:
        return {"success": False, "message": "Erro ao criar conta do paciente."}

    # Registrar a relação profissional-paciente no banco 'pacientes'
    paciente_response = supabase_client.table("pacientes").insert({
        "profissional": profissional,
        "paciente": paciente_username,
        "data_cadastro": "now()"
    }).execute()

    if paciente_response.error:
        return {"success": False, "message": "Erro ao cadastrar paciente na base de dados."}

    return {"success": True, "message": "Paciente cadastrado com sucesso!"}

def get_user_credentials(username):
    """ Obtém as credenciais do usuário (senha e tipo de usuário) a partir do banco de dados """
    response = supabase_client.table("users").select("password", "user_type").eq("username", username).execute()
    
    if response.data:
        return {
            "password": response.data[0]["password"],
            "user_type": response.data[0]["user_type"]
        }
    return None  # Retorna None se o usuário não existir

def insert_user(username, hashed_password, user_type):
    """ Insere um novo usuário no banco de dados """
    response = supabase_client.table("users").insert({
        "username": username,
        "password": hashed_password,
        "user_type": user_type
    }).execute()
    
    if response.error:
        return False  # Retorna False se houver erro
    return True  # Retorna True se o usuário for inserido com sucesso

def check_user_exists(username):
    """ Verifica se um usuário já está cadastrado no banco de dados """
    response = supabase_client.table("users").select("username").eq("username", username).execute()
    return bool(response.data)  # Retorna True se o usuário existir, False caso contrário


