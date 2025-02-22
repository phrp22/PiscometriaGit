import streamlit as st
import bcrypt
from database import check_user_exists, insert_user, supabase_client  # Importando supabase_client corretamente

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
            try:
                response = supabase_client.table("users").select("password").eq("username", username).execute()
                
                if response.data:
                    stored_password = response.data[0]["password"]
                    if check_password(stored_password, password):
                        st.success(f"Bem-vindo, {username}!")
                    else:
                        st.error("Senha incorreta.")
                else:
                    st.error("Usuário não encontrado.")
            except Exception as e:
                st.error(f"Erro ao buscar usuário: {str(e)}")
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
            
            try:
                # Verificar se o usuário já existe usando database.py
                if check_user_exists(new_username):
                    st.error("Nome de usuário já está em uso. Escolha outro.")
                    return
                
                # Se não existir, inserir no banco de dados usando database.py
                response = insert_user(new_username, hashed_password)
                
                if response:
                    st.success("Registro concluído com sucesso! Agora você pode fazer login.")
                else:
                    st.error("Erro ao registrar. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao registrar usuário: {str(e)}")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

if __name__ == "__main__":
    main()
