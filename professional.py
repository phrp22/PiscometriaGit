import uuid
import streamlit as st
from auth import supabase_client  # Certifique-se de que supabase_client está exportado no auth.py

def is_professional_enabled(email):
    response = supabase_client.from_("professional").select("*").eq("email", email).execute()
    try:
        data = response.data
    except Exception as e:
        st.error("Erro ao consultar área profissional: " + str(e))
        return False
    if data and len(data) > 0:
        return data[0].get("area_habilitada", False)
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

import streamlit as st
from auth import get_user, sign_out

import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area

def render_professional_sidebar(user):
    """Renderiza a sidebar para usuários com área profissional habilitada."""
    with st.sidebar:
        # Exibe uma mensagem de sucesso com mais "V" para enfatizar o status
        st.success("Área do profissional habilitada! VVVVV")
        st.write(f"Bem-vindo, {user['display_name']}!")
        st.write(f"Email: {user['email']}")
        
        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

def render_dashboard():
    """Renderiza o dashboard para usuários autenticados."""
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Se o usuário já tem a área profissional habilitada, usamos a sidebar específica
    if is_professional_enabled(user["email"]):
        render_professional_sidebar(user)
    else:
        # Aqui você pode exibir a sidebar padrão ou outro conteúdo
        with st.sidebar:
            st.title("🔑 Bem-vindo!")
            st.write(f"👤 {user['display_name']} ({user['email']})")
            if st.button("🚪 Sair"):
                sign_out()
                st.success("Você saiu com sucesso!")
                st.session_state["refresh"] = True
                st.rerun()

    # Conteúdo principal do dashboard
    st.title(f"🎉 Bem-vindo, {user['display_name']}!")
    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")
