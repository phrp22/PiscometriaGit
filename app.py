import streamlit as st
from auth import authenticate_user, register_user
from database import supabase_client

def main():
    st.title("Bem-vindo ao App")
    
    # Escolha entre Login e Registro
    choice = st.radio("Selecione uma opção:", ["Login", "Registro"])
    
    if choice == "Login":
        login()
    elif choice == "Registro":
        register()

def login():
    st.subheader("Tela de Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username and password:
            if authenticate_user(username, password):
                st.success(f"Bem-vindo, {username}!")
            else:
                st.error("Usuário ou senha incorretos.")
        else:
            st.error("Por favor, preencha os campos de usuário e senha.")

def register():
    st.subheader("Tela de Registro")
    new_username = st.text_input("Escolha um nome de usuário")
    new_password = st.text_input("Escolha uma senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")

    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            response = register_user(new_username, new_password)
            if response.get("status_code") == 201:
                st.success("Registro concluído com sucesso! Agora você pode fazer login.")
            else:
                st.error("Erro ao registrar. Tente um nome de usuário diferente.")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

if __name__ == "__main__":
    main()