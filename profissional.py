import streamlit as st
from database import cadastrar_paciente, listar_pacientes, enviar_escala  # ✅ Corrigimos os imports
from escalas import listar_escalas  # ✅ Importamos a lista de escalas

def profissional_dashboard():
    st.title("Área do Profissional")

    # Verifica se o usuário está autenticado e é um profissional
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return
    if st.session_state.user_type != "Profissional":
        st.error("Acesso restrito a profissionais.")
        return

def enviar_escala_interface():
    st.subheader("Enviar Escala Psicométrica")

    # Selecionar um paciente cadastrado
    pacientes = listar_pacientes(st.session_state.username)
    if not pacientes:
        st.warning("Nenhum paciente cadastrado ainda.")
        return

    paciente_selecionado = st.selectbox("Escolha um paciente:", [p["paciente"] for p in pacientes])

    # Selecionar uma escala disponível
    escalas_disponiveis = listar_escalas()
    escala_selecionada = st.selectbox("Escolha uma escala:", escalas_disponiveis)

    if st.button("Enviar Escala"):
        response = enviar_escala(st.session_state.username, paciente_selecionado, escala_selecionada)
        if response:
            st.success(f"Escala '{escala_selecionada}' enviada para {paciente_selecionado} com sucesso!")
        else:
            st.error("Erro ao enviar a escala.")

def cadastrar_paciente_interface():
    st.subheader("Cadastrar Novo Paciente")
    
    paciente_username = st.text_input("Nome de Usuário do Paciente")
    paciente_password = st.text_input("Senha do Paciente", type="password")

    if st.button("Cadastrar Paciente"):
        if paciente_username and paciente_password:
            response = cadastrar_paciente(st.session_state.username, paciente_username, paciente_password)
            if response["success"]:
                st.success(response["message"])
            else:
                st.error(response["message"])
        else:
            st.error("Preencha todos os campos!")

if __name__ == "__main__":
    profissional_dashboard()


    