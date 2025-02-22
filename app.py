import streamlit as st
import bcrypt
from database import check_user_exists, insert_user, supabase_client

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

    # Inicializa session_state se ainda não estiver definido
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.session_state.username = None

    # Se o usuário já estiver autenticado, direciona para a interface correspondente
    if st.session_state.authenticated:
        if st.session_state.user_type == "Profissional":
            profissional_interface()
        else:
            paciente_interface()
    else:
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
                stored_password, user_type = get_user_credentials(username)  # Agora pegamos a senha e o tipo de usuário

                if stored_password:
                    if check_password(stored_password, password):
                        st.success(f"Bem-vindo, {username}!")

                        # Usando st.session_state para armazenar o user_type
                        st.session_state["user_type"] = user_type

                        # Redirecionamento sem sidebar
                        if user_type == "Profissional":
                            st.session_state["page"] = "profissional"
                        else:
                            st.session_state["page"] = "paciente"
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
    user_type = st.radio("Você é um:", ["Profissional", "Paciente"])  # Novo campo
    
    if st.button("Registrar"):
        if new_username and new_password and new_password == confirm_password:
            hashed_password = hash_password(new_password)
            
            try:
                if check_user_exists(new_username):
                    st.error("Nome de usuário já está em uso. Escolha outro.")
                    return
                
                response = insert_user(new_username, hashed_password, user_type)  # Adicionado user_type
                
                if response:
                    st.success("Registro concluído com sucesso! Agora você pode fazer login.")
                else:
                    st.error("Erro ao registrar. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao registrar usuário: {str(e)}")
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

def profissional_interface():
    st.subheader("Área do Profissional")
    st.write(f"Bem-vindo, {st.session_state.username}! Aqui estão suas opções:")
    # Adicione elementos específicos para profissionais aqui

def paciente_interface():
    st.subheader("Área do Paciente")
    st.write(f"Bem-vindo, {st.session_state.username}! Aqui estão suas opções:")
    # Adicione elementos específicos para pacientes aqui

if __name__ == "__main__":
    main()