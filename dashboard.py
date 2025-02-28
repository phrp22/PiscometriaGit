import streamlit as st
from auth import sign_out, get_user

def render_sidebar(user):
    """Renderiza a sidebar para usuários logados."""
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.write(f"👤 Usuário: {user['email']}")  

        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

def render_dashboard():
    """Renderiza o dashboard para usuários autenticados."""
    
    user = get_user()  # 📌 Obtém o usuário logado

    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # 🛠️ Ativa a sidebar apenas no dashboard
    render_sidebar(user)

    # 📌 Título do Dashboard
    st.title(f"🎉 Bem-vindo, {user['email']}!")

    # 📊 Estatísticas fictícias no dashboard
    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")
