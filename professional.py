import uuid
import streamlit as st
from auth import supabase_client  # Certifique-se de que supabase_client está exportado no auth.py

def is_professional_enabled(email):
    """
    Consulta a tabela 'professional' no Supabase para verificar se o usuário
    com o email informado tem a área profissional habilitada.
    """
    response = supabase_client.from_("professional").select("*").eq("email", email).execute()

    # 📌 Verifica se há erro na resposta do Supabase
    if hasattr(response, "data") and response.data is not None:
        data = response.data
        if data and len(data) > 0:
            return data[0].get("area_habilitada", False)
        return False
    else:
        st.error(f"Erro ao consultar área profissional: {response}")
        return False


def enable_professional_area(email, display_name):
    """
    Insere um registro na tabela 'professional' no Supabase para habilitar a área do profissional.
    """
    new_uuid = str(uuid.uuid4())
    data = {
        "id": new_uuid,
        "email": email,
        "display_name": display_name,
        "area_habilitada": True
    }
    response = supabase_client.from_("professional").insert(data).execute()
    if response.error:
        return False, response.error.message
    return True, "Área do profissional habilitada com sucesso!"

def render_professional_dashboard():
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    st.title("Dashboard Profissional")
    st.markdown("### Bem-vindo à área profissional!")
    st.markdown("Aqui você pode acessar funcionalidades exclusivas para profissionais da saúde mental.")
    # Adicione aqui os widgets e estatísticas específicas para profissionais