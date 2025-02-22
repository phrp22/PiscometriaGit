import supabase
import streamlit as st
import json

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


def listar_respostas_pacientes(profissional_username):
    """Retorna todas as respostas das escalas enviadas pelo profissional."""
    response = supabase_client.table("respostas_escalas").select(
        "paciente", "escala", "respostas", "criado_em"
    ).eq("profissional", profissional_username).execute()

    if not response.data:
        return []  # Se não houver respostas, retorna uma lista vazia

    return response.data  # Retorna as respostas disponíveis


def listar_escalas_pendentes(paciente_username):
    """Retorna apenas as escalas que ainda não foram respondidas pelo paciente."""
    
    # Buscar todas as escalas enviadas para o paciente
    escalas_enviadas = supabase_client.table("escalas_enviadas").select("escala").eq("paciente", paciente_username).execute()
    
    if not escalas_enviadas.data:
        return []  # Se não houver escalas enviadas, retorna uma lista vazia

    # Buscar todas as escalas que o paciente já respondeu
    escalas_respondidas = supabase_client.table("respostas_escalas").select("escala").eq("paciente", paciente_username).execute()
    
    # Criar listas com os nomes das escalas
    enviadas = {item["escala"] for item in escalas_enviadas.data}  # Conjunto de escalas enviadas
    respondidas = {item["escala"] for item in escalas_respondidas.data}  # Conjunto de escalas respondidas

    # Escalas pendentes são as enviadas menos as já respondidas
    escalas_pendentes = list(enviadas - respondidas)

    return escalas_pendentes


def get_profissional_da_escala(paciente_username, escala):
    """Obtém o nome do profissional que enviou a escala para o paciente."""
    
    response = supabase_client.table("escalas_enviadas").select("profissional").eq("paciente", paciente_username).eq("escala", escala).execute()

    if not response.data or len(response.data) == 0:
        st.error(f"Erro: Nenhum profissional encontrado para a escala '{escala}' enviada ao paciente '{paciente_username}'.")
        return None  # Retorna None se não encontrar um profissional associado
    
    profissional = response.data[0]["profissional"]
    st.write(f"Profissional encontrado: {profissional}")  # ✅ Log para depuração
    return profissional



def listar_escalas_paciente(paciente_username):
    """Retorna a lista de escalas enviadas para um paciente."""
    response = supabase_client.table("escalas_enviadas").select("escala").eq("paciente", paciente_username).execute()
    
    if response.data:
        return [item["escala"] for item in response.data]
    
    return []  # Retorna uma lista vazia se nenhuma escala foi enviada

def salvar_respostas_escala(paciente_username, escala, respostas):
    """Salva as respostas do paciente e adiciona o profissional responsável."""
    
    profissional_responsavel = get_profissional_da_escala(paciente_username, escala)
    
    if not profissional_responsavel:
        st.error("Erro: Nenhum profissional encontrado para essa escala.")
        return False

    try:
        response = supabase_client.table("respostas_escalas").insert({
            "paciente": paciente_username,
            "profissional": profissional_responsavel,  # ✅ Agora armazenamos o profissional
            "escala": escala,
            "respostas": json.dumps(respostas),  # ✅ Converte dicionário para JSON
            "criado_em": "now()"  # ✅ Salva o timestamp atual
        }).execute()

        return response.data is not None  # Retorna True se o insert foi bem-sucedido

    except Exception as e:
        st.error(f"Erro ao salvar respostas no banco: {str(e)}")  # ✅ Exibe erro detalhado no app
        return False



def enviar_escala(profissional, paciente, escala):
    """Registra o envio de uma escala psicométrica para um paciente"""
    response = supabase_client.table("escalas_enviadas").insert({
        "profissional": profissional,
        "paciente": paciente,
        "escala": escala
    }).execute()
    return response

def get_profissional_uuid(profissional_username):
    """Obtém o UUID do profissional baseado no nome de usuário."""
    response = supabase_client.table("users").select("id").eq("username", profissional_username).execute()
    
    if response.data:
        return response.data[0]["id"]  # Retorna o UUID do profissional
    
    return None  # Retorna None se o usuário não for encontrado

def get_user_uuid(username):
    """Obtém o UUID do usuário com base no nome de usuário."""
    response = supabase_client.table("users").select("id").eq("username", username).execute()
    if response.data:
        return response.data[0]["id"]
    return None

def cadastrar_paciente(profissional_username, paciente_username, paciente_password):
    """Autentica um paciente antes de cadastrá-lo ao profissional e insere na tabela pacientes."""
    
    from auth import check_password  # ✅ Importação dentro da função para evitar ciclo

    # Obtém o UUID do profissional
    profissional_uuid = get_user_uuid(profissional_username)
    if not profissional_uuid:
        return {"success": False, "message": "Erro: Profissional não encontrado no banco de dados."}

    # Autentica o paciente
    user_data = get_user_credentials(paciente_username)
    
    if user_data and "password" in user_data and check_password(user_data["password"], paciente_password):
        # Verifica se o paciente já está vinculado
        existing = supabase_client.table("pacientes").select("*").eq("paciente", paciente_username).execute()
        
        if existing.data:
            return {"success": False, "message": "Paciente já está vinculado a um profissional."}

        # Insere o paciente na tabela 'pacientes' usando o UUID do profissional
        response = supabase_client.table("pacientes").insert({
            "profissional": profissional_uuid,
            "paciente": paciente_username
        }).execute()

        if response.data:
            return {"success": True, "message": "Paciente autenticado e vinculado ao profissional."}
        else:
            return {"success": False, "message": "Erro ao cadastrar paciente no banco de dados."}
    
    return {"success": False, "message": "Falha na autenticação. Verifique as credenciais do paciente."}

def listar_pacientes(profissional_username):
    """Lista pacientes cadastrados pelo profissional."""

    # Obtém o UUID do profissional
    profissional_uuid = get_profissional_uuid(profissional_username)
    
    if not profissional_uuid:
        st.error("Erro: Profissional não encontrado no banco de dados.")
        return []

    try:
        # Filtra os pacientes pelo UUID do profissional
        response = supabase_client.table("pacientes").select("paciente").eq("profissional", profissional_uuid).execute()

        if not response.data:
            return []  # Retorna uma lista vazia se não houver pacientes
        
        return response.data  # Retorna a lista de pacientes

    except Exception as e:
        st.error(f"Erro ao listar pacientes: {str(e)}")  # Exibe o erro no app
        return []

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