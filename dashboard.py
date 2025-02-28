import streamlit as st
from auth import get_user, sign_out  # 🔑 Funções de autenticação

def render_sidebar(user):
    """Renderiza a sidebar para usuários logados."""
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.write(f"👤 {user['display_name']} ({user['email']})")  # Exibe nome e email

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

    render_sidebar(user)  # Ativa a sidebar com os dados do usuário

    # 📌 Título do Dashboard
    st.title(f"🎉 Bem-vindo, {user['display_name']}!")

    # 📊 Estatísticas no dashboard
    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")
