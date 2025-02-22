import streamlit as st
from database import criar_usuario, login_usuario, get_user_by_id
import profissional
import paciente

def main():
    st.title("Bem-vindo ao App")

    if "user" in st.session_state and st.session_state.user:
        st.success(f"Usuário autenticado: {st.session_state.user['email']}")

        if st.session_state.user["user_type"] == "Profissional":
            profissional.profissional_page()  # Chama diretamente
        else:
            paciente.paciente_page()
        return

    choice = st.radio("Selecione uma opção:", ["Login", "Registro"])

    if choice == "Login":
        login()
    elif choice == "Registro":
        register()

def login():
    st.subheader("Tela de Login")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if email and password:
            user_data = login_usuario(email, password)

            if user_data and "user" in user_data:
                user_id = user_data["user"]["id"]  # Pega o UUID do usuário autenticado

                # Obtém informações adicionais do usuário no banco
                user_info = get_user_by_id(user_id)

                # Armazena os dados do usuário na sessão
                st.session_state.user = {
                    "id": user_id,
                    "email": user_data["user"]["email"],
                    "user_type": user_info.get("user_type", "Paciente")  # Default para Paciente se não encontrado
                }

                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

def register():
    st.subheader("Tela de Registro")
    email = st.text_input("Digite seu email")
    password = st.text_input("Digite sua senha", type="password", help="A senha deve ter pelo menos 6 caracteres.")
    confirm_password = st.text_input("Confirme sua senha", type="password")
    user_type = st.radio("Você é um:", ["Profissional", "Paciente"])

    if st.button("Registrar"):
        if email and password and password == confirm_password:
            response = criar_usuario(email, password)

            if response and "user" in response:
                st.success("Registro concluído com sucesso! Agora faça login.")
            else:
                st.error("Erro ao registrar usuário. Tente novamente.")
        else:
            st.error("As senhas não coincidem ou algum campo está vazio.")

if __name__ == "__main__":
    main()
