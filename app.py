import streamlit as st

def main():
    st.title("Login App")
    
    # Campos de entrada para login e senha
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    # Botão para submeter os dados
    if st.button("Login"):
        if username and password:
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Por favor, preencha os campos de usuário e senha.")

if __name__ == "__main__":
    main()