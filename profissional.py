import streamlit as st
from database import cadastrar_paciente, enviar_escala_psicometrica

def profissional_dashboard():
    st.title("Área do Profissional")

    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    if st.session_state.user_type != "Profissional":
        st.error("Acesso restrito a profissionais.")
        return

    st.subheader("Enviar Escala Psicométrica")
    
    paciente_username = st.text_input("Nome de Usuário do Paciente")
    escala = st.text_area("Digite a escala psicométrica")

    if st.button("Enviar Escala"):
        if paciente_username and escala:
            response = enviar_escala_psicometrica(st.session_state.username, paciente_username, escala)
            if response["success"]:
                st.success(response["message"])
            else:
                st.error(response["message"])
        else:
            st.error("Preencha todos os campos!")