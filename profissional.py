import streamlit as st
from database import cadastrar_paciente, listar_pacientes

def profissional_dashboard():
    st.title("Área do Profissional")

    # Verifica se o usuário está autenticado e é um profissional
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return
    if st.session_state.user_type != "Profissional":
        st.error("Acesso restrito a profissionais.")
        return

    st.subheader("Cadastrar Novo Paciente")
    
    paciente_username = st.text_input("Nome de Usuário do Paciente")
    paciente_password = st.text_input("Senha do Paciente", type="password")

    if st.button("Cadastrar Paciente"):
        if paciente_username and paciente_password:
            response = cadastrar_paciente(st.session_state.username, paciente_username, paciente_password)
            if response["success"]:
                st.success(response["message"])
                st.rerun()
            else:
                st.error(response["message"])
        else:
            st.error("Preencha todos os campos!")
    
    st.subheader("Pacientes Cadastrados")
    pacientes = listar_pacientes(st.session_state.username)
    if pacientes:
        for paciente in pacientes:
            st.write(f"{paciente}")
    else:
        st.write("Nenhum paciente cadastrado ainda.")

if __name__ == "__main__":
    profissional_dashboard()
