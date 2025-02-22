import streamlit as st
from database import cadastrar_paciente

def profissional_dashboard():
    st.title("Área do Profissional")

    # Verifica se o usuário está autenticado e é um profissional
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return
    if st.session_state.user_type != "Profissional":
        st.error("Acesso restrito a profissionais.")
        return

    # Adicionando opção no menu lateral
    opcao = st.sidebar.selectbox("Menu", ["Cadastrar Paciente", "Enviar Escala Psicométrica"])

    if opcao == "Cadastrar Paciente":
        cadastrar_paciente_interface()  # Mantemos o cadastro de paciente

    elif opcao == "Enviar Escala Psicométrica":
        enviar_escala_interface()  # Função que criará a interface de envio

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

if __name__ == "__main__":
    profissional_dashboard()

    