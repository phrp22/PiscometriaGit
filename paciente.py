import streamlit as st

def paciente_page():
    st.title("Área do Paciente")
    st.write(f"Bem-vindo, {st.session_state.username}!")
