import streamlit as st

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
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Por favor, preencha os campos de usuário e senha.")

def register():
    st.subheader("Tela de Registro")
    new_username = st.text_input("Escolha um nome de usuário")
    new_password = st.text_input("Escolha uma senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")
    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            st.success("Registro concluído com sucesso! Agora você pode fazer login.")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

if __name__ == "__main__":
    main()
