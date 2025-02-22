import streamlit as st
from database import insert_paciente

def profissional_page():
    st.title("Área do Profissional")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    st.subheader("Cadastrar Paciente")
    paciente_nome = st.text_input("Nome do Paciente")

    if st.button("Adicionar Paciente"):
        if paciente_nome:
            try:
                response = insert_paciente(st.session_state.username, paciente_nome)
                st.success(f"Paciente {paciente_nome} cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar paciente: {str(e)}")
        else:
            st.error("O nome do paciente não pode estar vazio.")

    if st.button("Sair"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.rerun()