import streamlit as st
import bcrypt
from database import get_user_credentials, insert_user, check_user_exists

def hash_password(password):
    """ Gera um hash seguro para a senha """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_password, provided_password):
    """ Verifica se a senha digitada corresponde ao hash armazenado """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def main():
    st.title("Academia Diagnóstica")

    # Verifica se o usuário já está autenticado
    if "authenticated" in st.session_state and st.session_state.authenticated:
        if st.session_state.user_type == "Profissional":
            import profissional
            profissional.profissional_page()
        else:
            import paciente
            paciente.paciente_page()
        return

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
                user_data = get_user_credentials(username)
                if user_data:
                    stored_password = user_data["password"]
                    user_type = user_data["user_type"]

                    if check_password(stored_password, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_type = user_type
                        st.rerun()  # Recarrega a página para redirecionar
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
    user_type = st.radio("Você é um:", ["Profissional", "Paciente"])

    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            hashed_password = hash_password(new_password)
            try:
                if check_user_exists(new_username):
                    st.error("Nome de usuário já está em uso. Escolha outro.")
                    return

                response = insert_user(new_username, hashed_password, user_type)
                
                if response and not response.get("error"):  # Garante que não houve erro na inserção
                    st.success("Registro concluído com sucesso! Agora você pode fazer login.")
                else:
                    st.error("Erro ao registrar. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao registrar usuário: {str(e)}")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

