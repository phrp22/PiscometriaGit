import streamlit as st

def paciente_page():
    st.title("Área do Paciente")

    # Verifica se o usuário está autenticado antes de exibir o conteúdo
    if "user" not in st.session_state or not st.session_state.user:
        st.error("Você precisa estar autenticado para acessar esta página.")
        return

    st.write(f"Bem-vindo, {st.session_state.user['email']}!")  # Exibe o e-mail do usuário

    if st.button("Sair"):
        st.session_state.user = None  # Reseta a sessão do usuário
        st.rerun()
