import supabase
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def cadastrar_paciente(profissional_username, paciente_nome):
    """Registra um paciente vinculado a um profissional."""
    response = supabase_client.table("pacientes").insert({
        "profissional": profissional_username,
        "paciente": paciente_nome,
        "data_cadastro": "now()"
    }).execute()
    return response

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