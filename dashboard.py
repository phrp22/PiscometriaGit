import streamlit as st
from auth import sign_out, get_user

def render_dashboard():
    """Renderiza o dashboard para usuários autenticados."""

    user = get_user()

    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # 🛠️ Sidebar com o nome do usuário
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.write(f"👤 {user['display_name']} ({user['email']})")  # Nome do usuário!

        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

    # 📌 Título do Dashboard
    st.title(f"🎉 Olá, {user['display_name']}!")

    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")
