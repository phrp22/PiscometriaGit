import streamlit as st
from database import insert_paciente

def profissional_page():
    st.title("Área do Profissional")

    # Verifica se o usuário está autenticado antes de exibir o conteúdo
    if "user" not in st.session_state or not st.session_state.user:
        st.error("Você precisa estar autenticado para acessar esta página.")
        return

    st.write(f"Bem-vindo, {st.session_state.user['email']}!")  # Exibe o e-mail do usuário

    st.subheader("Cadastrar Paciente")
    paciente_nome = st.text_input("Nome do Paciente")

    if st.button("Adicionar Paciente"):
        if paciente_nome:
            try:
                response = insert_paciente(st.session_state.user["id"], paciente_nome)  # Agora usa o UUID do profissional
                st.success(f"Paciente {paciente_nome} cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar paciente: {str(e)}")
        else:
            st.error("O nome do paciente não pode estar vazio.")

    if st.button("Sair"):
        st.session_state.user = None  # Reseta a sessão do usuário
        st.rerun()
