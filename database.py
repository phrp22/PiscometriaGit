import supabase
import streamlit as st
import bcrypt

# Conexão com o Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def check_password(stored_password, provided_password):
    """Verifica se a senha digitada corresponde ao hash armazenado."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def check_user_exists(username):
    """Verifica se um usuário já está cadastrado."""
    try:
        response = supabase_client.table("users").select("username").eq("username", username).execute()
        return bool(response.data and len(response.data) > 0)
    except Exception as e:
        print(f"Erro ao verificar usuário: {str(e)}")
        return False

def insert_user(username, hashed_password, user_type):
    """Insere um novo usuário no banco de dados."""
    try:
        response = supabase_client.table("users").insert({
            "username": username,
            "password": hashed_password,
            "user_type": user_type
        }).execute()
        
        if response.data:
            return {"success": True, "message": "Usuário cadastrado com sucesso!"}
        else:
            return {"success": False, "message": "Erro ao cadastrar usuário no banco de dados."}
    
    except Exception as e:
        return {"success": False, "message": f"Erro ao inserir usuário: {str(e)}"}

def get_user_credentials(username):
    """Obtém senha e tipo de usuário pelo nome de usuário."""
    try:
        response = supabase_client.table("users").select("password", "user_type").eq("username", username).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"Erro ao buscar credenciais do usuário: {str(e)}")
    return None

def get_user_uuid(username):
    """Obtém o UUID do usuário com base no nome de usuário."""
    try:
        response = supabase_client.table("users").select("id").eq("username", username).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["id"]
        else:
            print(f"Usuário '{username}' não encontrado.")
    except Exception as e:
        print(f"Erro ao obter UUID do usuário: {str(e)}")
    return None
