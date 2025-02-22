import supabase
import streamlit as st
from database import get_user_uuid, get_user_credentials, check_password


# Conexão com o Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def cadastrar_paciente(profissional_username, paciente_username, paciente_password):
    """Autentica um paciente antes de cadastrá-lo ao profissional e insere na tabela pacientes."""
    
    profissional_uuid = get_user_uuid(profissional_username)
    if not profissional_uuid:
        return {"success": False, "message": "Erro: Profissional não encontrado no banco de dados."}

    user_data = get_user_credentials(paciente_username)
    if user_data and check_password(user_data["password"], paciente_password):
        
        # Verifica se o paciente já está vinculado
        try:
            existing = supabase_client.table("pacientes").select("*").eq("paciente", paciente_username).execute()
            if existing.data:
                return {"success": False, "message": "Paciente já está vinculado a um profissional."}

            # Insere o paciente na tabela 'pacientes'
            response = supabase_client.table("pacientes").insert({
                "profissional": profissional_uuid,
                "paciente": paciente_username
            }).execute()

            if response.data:
                return {"success": True, "message": "Paciente autenticado e vinculado ao profissional."}
            else:
                return {"success": False, "message": "Erro ao cadastrar paciente no banco de dados."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao acessar banco: {str(e)}"}

    return {"success": False, "message": "Falha na autenticação. Verifique as credenciais do paciente."}

def listar_pacientes(profissional_username):
    """Lista pacientes cadastrados pelo profissional."""
    profissional_uuid = get_user_uuid(profissional_username)
    if not profissional_uuid:
        return []

    try:
        response = supabase_client.table("pacientes").select("paciente, data_cadastro").eq("profissional", profissional_uuid).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao listar pacientes: {str(e)}")
        return []
