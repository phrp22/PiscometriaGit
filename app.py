import streamlit as st
from auth import authenticate_user, register_user
from database import check_user_exists
from utils import hash_password
import profissional
import paciente

def main():
    st.title("Bem-vindo ao App")

    # Se o usuário já está autenticado, direciona para o dashboard
    if "authenticated" in st.session_state and st.session_state.authenticated:
        navigate_to_dashboard()
        return

    # Remover qualquer barra lateral automática
    st.set_page_config(layout="centered")

    choice = st.radio("Selecione uma opção:", ["Login", "Registro"])
    
    if choice == "Login":
        login()
    elif choice == "Registro":
        register()

def navigate_to_dashboard():
    """Redireciona para a página correspondente ao tipo de usuário"""
    if st.session_state.user_type == "Profissional":
        profissional.profissional_page()
    else:
        paciente.paciente_page()

def login():
    st.subheader("Tela de Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        authenticated, user_type = authenticate_user(username, password)
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_type = user_type
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def register():
    st.subheader("Tela de Registro")
    new_username = st.text_input("Nome de usuário")
    new_password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")
    user_type = st.radio("Você é um:", ["Profissional", "Paciente"])

    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            if check_user_exists(new_username):
                st.error("Nome de usuário já está em uso.")
                return
            register_user(new_username, new_password, user_type)
            st.success("Registro bem-sucedido! Agora você pode fazer login.")
        else:
            st.error("Preencha todos os campos corretamente.")

if __name__ == "__main__":
    main()
