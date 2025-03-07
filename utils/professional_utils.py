import streamlit as st
from auth import supabase_client, sign_out
from patient_link import create_patient_invitation 


# 💾 Função para cachear o estado da área profissional.
@st.cache_data
def get_professional_data(auth_user_id):
    
    # Busca os dados do usuário no banco de dados <professional>
    response = supabase_client.from_("professional") \
        .select("auth_user_id, area_habilitada") \
        .eq("auth_user_id", auth_user_id) \
        .execute()

    # Se houver algum registro...
    if response and hasattr(response, "data") and response.data:
        return response.data[0]  # Retorna um booleano.
    return None  # Se não, retorna o conjunto vazio.


# 🩺 Função para verificar se a área do profissional está habilitada.
def is_professional_enabled(auth_user_id):

    # Verifica, sem gastar requisições ao banco de dados, se a área está ativa ou não.
    professional_data = get_professional_data(auth_user_id)

    # Se houver algum registro...
    if professional_data:
        return professional_data.get("area_habilitada", False)  # Retorna um booleano.
    return False  # Se não, retorna uma resposta negativa.


# ⚒️ Função para habilitar área do profissional.
def enable_professional_area(auth_user_id, email, display_name):

    # Verifica, sem gastar requisições ao banco de dados, se a área está ativa ou não.
    professional_data = get_professional_data(auth_user_id) 

    # Se houver algum registro...
    if professional_data:
        # Basta atualizar.
        update_response = supabase_client.from_("professional") \
            .update({"area_habilitada": True}) \
            .eq("auth_user_id", auth_user_id) \
            .execute()

        # Se der erro...
        if hasattr(update_response, "error") and update_response.error:
            return False, f"Erro ao atualizar: {update_response.error.message}"  # Vamos avisar.
        
        return True, None  # Caso constrário, já pode comemorar.

    # Quando não houver registro, um dicionário será criado.
    data = {
        "auth_user_id": auth_user_id,  # O UUID é o identificador principal
        "email": email,
        "display_name": display_name,
        "area_habilitada": True
    }
    
    # Insere o dicionário no banco de dados <professional>
    insert_response = supabase_client.from_("professional") \
        .insert(data) \
        .execute()

    # Se der erro...
    if hasattr(insert_response, "error") and insert_response.error:
        return False, f"Erro ao criar registro: {insert_response.error.message}"  # Vamos avisar.
    
    return True, None # Caso constrário, já pode comemorar.

