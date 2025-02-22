import streamlit as st
import bcrypt
import supabase

# Conectar ao Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password):
    """ Gera um hash seguro para a senha """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_password, provided_password):
    """ Verifica se a senha digitada corresponde ao hash armazenado """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

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
            response = supabase_client.table("users").select("password").eq("username", username).execute()
            
            if response.data:
                stored_password = response.data[0]["password"]
                if check_password(stored_password, password):
                    st.success(f"Bem-vindo, {username}!")
                else:
                    st.error("Senha incorreta.")
            else:
                st.error("Usuário não encontrado.")
        else:
            st.error("Por favor, preencha os campos de usuário e senha.")

def register():
    st.subheader("Tela de Registro")
    new_username = st.text_input("Escolha um nome de usuário")
    new_password = st.text_input("Escolha uma senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")
    
    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            hashed_password = hash_password(new_password)
            
            response = supabase_client.table("users").insert({
                "username": new_username,
                "password": hashed_password
            }).execute()
            
            if response.get("status_code") == 201:
                st.success("Registro concluído com sucesso! Agora você pode fazer login.")
            else:
                st.error("Erro ao registrar. Tente um nome de usuário diferente.")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

if __name__ == "__main__":
    main()
