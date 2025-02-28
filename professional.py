import uuid
import streamlit as st


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

def render_professional_sidebar(user):
    """Renderiza a sidebar para a dashboard profissional."""
    with st.sidebar:
        st.title("Área Profissional Habilitada")
        st.write(f"Bem-vindo, {user['display_name']}!")
        st.write(f"Email: {user['email']}")
        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

def render_professional_dashboard():
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta área.")
        return

    render_professional_sidebar(user)
    
    # Conteúdo principal do dashboard profissional:
    st.title("Dashboard Profissional")
    st.markdown("### Funcionalidades exclusivas para profissionais")
    st.markdown("Aqui você pode acessar relatórios, configurar sua área, e muito mais!")
    # Adicione aqui os widgets e funcionalidades específicas para profissionais.
