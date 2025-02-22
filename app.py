import streamlit as st
import profissional
from database import get_user_credentials, insert_user, check_user_exists
from auth import authenticate_user, register_user  # Importando funções do auth.py

def main():
    st.title("Academia Diagnóstica")

    # Verifica se o usuário já está autenticado
    if not st.session_state.get("authenticated", False):
        choice = st.radio("Selecione uma opção:", ["Login", "Registro"])

        if choice == "Login":
            login()
        elif choice == "Registro":
            register()
        return

    # Botão de logout na barra lateral
    st.sidebar.button("Sair", on_click=logout)

    # Menu para PROFISSIONAIS
    if st.session_state.user_type == "Profissional":
        opcao = st.sidebar.selectbox("Menu", ["Cadastrar Paciente", "Enviar Escalas", "Ver Respostas"])  # ✅ Nova opção

        if opcao == "Cadastrar Paciente":
            profissional.cadastrar_paciente_interface()
        elif opcao == "Enviar Escalas":
            profissional.enviar_escala_interface()
        elif opcao == "Ver Respostas":
            profissional.ver_respostas_interface()  # ✅ Agora o profissional pode ver as respostas

    # Menu para PACIENTES
    elif st.session_state.user_type == "Paciente":
        import paciente
        opcao = st.sidebar.selectbox("Menu", ["Responder Escalas"])  # ✅ Paciente só vê as escalas pendentes

        if opcao == "Responder Escalas":
            paciente.paciente_page()  # ✅ O paciente agora pode responder escalas normalmente

def login():
    st.subheader("Tela de Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username and password:
            try:
                authenticated, user_type = authenticate_user(username, password)  # Chamando auth.py corretamente
                if authenticated:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_type = user_type
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
            except Exception as e:
                st.error(f"Erro ao buscar usuário: {str(e)}")
        else:
            st.error("Por favor, preencha os campos de usuário e senha.")

def register():
    st.subheader("Tela de Registro")
    new_username = st.text_input("Escolha um nome de usuário")
    new_password = st.text_input("Escolha uma senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")
    user_type = st.radio("Você é um:", ["Profissional", "Paciente"])

    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            try:
                if check_user_exists(new_username):
                    st.error("Nome de usuário já está em uso. Escolha outro.")
                    return
                
                response = register_user(new_username, new_password, user_type)  # Agora chamando auth.py corretamente
                if response:
                    st.success("Registro concluído com sucesso! Agora você pode fazer login.")
                else:
                    st.error("Erro ao registrar. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao registrar usuário: {str(e)}")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

def logout():
    """Desloga o usuário"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_type = None  # ✅ Removemos st.rerun()

if __name__ == "__main__":
    main()
