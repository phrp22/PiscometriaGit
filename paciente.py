import streamlit as st

def paciente_page():
    st.title("Área do Paciente")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    if st.button("Sair"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.rerun()
