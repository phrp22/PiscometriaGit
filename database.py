import supabase
import streamlit as st
import bcrypt

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


def listar_escalas(paciente_username):
    """Lista as escalas enviadas para um paciente."""
    response = supabase_client.table("escalas").select("escala", "status").eq("paciente", paciente_username).execute()
    return response.data if response.data else []

def atualizar_status_escala(paciente_username, escala):
    """Atualiza o status da escala para 'concluído'."""
    response = supabase_client.table("escalas").update({"status": "concluído"}).eq("paciente", paciente_username).eq("escala", escala).execute()
    return response

def listar_pacientes(profissional_username):
    """Lista os pacientes vinculados a um profissional."""
    response = supabase_client.table("pacientes").select("paciente").eq("profissional", profissional_username).execute()
    return response.data if response.data else []

def enviar_escala(profissional_username, paciente_username, escala):
    """Registra o envio de uma escala psicométrica para um paciente."""
    profissional_uuid = get_user_uuid(profissional_username)

    if not profissional_uuid:
        return {"success": False, "message": "Erro: Profissional não encontrado."}

    response = supabase_client.table("escalas").insert({
        "profissional": profissional_uuid,
        "paciente": paciente_username,
        "escala": escala,
        "status": "pendente"
    }).execute()

    if response.data:
        return {"success": True, "message": "Escala enviada com sucesso!"}
    return {"success": False, "message": "Erro ao enviar escala."}

def check_password(stored_password, provided_password):
    """Verifica se a senha digitada corresponde ao hash armazenado."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def get_user_uuid(username):
    """Obtém o UUID do usuário com base no nome de usuário."""
    response = supabase_client.table("users").select("id").eq("username", username).execute()
    if response.data:
        return response.data[0]["id"]
    return None

def cadastrar_paciente(profissional_username, paciente_username, paciente_password):
    """Autentica um paciente antes de cadastrá-lo ao profissional e insere na tabela pacientes."""
    
    # Obtém o UUID do profissional
    profissional_uuid = get_user_uuid(profissional_username)
    if not profissional_uuid:
        return {"success": False, "message": "Erro: Profissional não encontrado no banco de dados."}

    # Autentica o paciente
    user_data = get_user_credentials(paciente_username)
    
    if user_data and check_password(user_data["password"], paciente_password):
        # Verifica se o paciente já está vinculado
        existing = supabase_client.table("pacientes").select("*").eq("paciente", paciente_username).execute()
        
        if existing.data:
            return {"success": False, "message": "Paciente já está vinculado a um profissional."}

        # Insere o paciente na tabela 'pacientes' usando o UUID do profissional
        response = supabase_client.table("pacientes").insert({
            "profissional": profissional_uuid,  # Agora usamos o UUID corretamente
            "paciente": paciente_username
        }).execute()

        if response.data:
            return {"success": True, "message": "Paciente autenticado e vinculado ao profissional."}
        else:
            return {"success": False, "message": "Erro ao cadastrar paciente no banco de dados."}
    
    return {"success": False, "message": "Falha na autenticação. Verifique as credenciais do paciente."}

def listar_pacientes(profissional_username):
    """Lista pacientes cadastrados pelo profissional."""
    response = supabase_client.table("pacientes").select("paciente, data_cadastro").eq("profissional", profissional_username).execute()
    return response.data if response.data else []

# profissional.py - Adicionando formulário de cadastro
import streamlit as st
from database import cadastrar_paciente, listar_pacientes

def profissional_page():
    st.title("Área do Profissional")
    st.write(f"Bem-vindo, {st.session_state.username}!")
    
    st.subheader("Cadastrar Novo Paciente")
    paciente_nome = st.text_input("Nome do Paciente")
    
    if st.button("Cadastrar Paciente"):
        if paciente_nome:
            response = cadastrar_paciente(st.session_state.username, paciente_nome)
            if response:
                st.success(f"Paciente {paciente_nome} cadastrado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar paciente.")
        else:
            st.error("O nome do paciente não pode estar vazio.")
    
    st.subheader("Pacientes Cadastrados")
    pacientes = listar_pacientes(st.session_state.username)
    if pacientes:
        for paciente in pacientes:
            st.write(f"{paciente['paciente']} - Cadastrado em: {paciente['data_cadastro']}")
    else:
        st.write("Nenhum paciente cadastrado ainda.")
    
    if st.button("Sair"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.rerun()

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