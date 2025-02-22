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

def register_user(username, password, user_type):
    """ Registra um novo usuário no Supabase Authentication e na tabela `users` """
    response = supabase.auth.sign_up({
        "email": username,  # O Supabase precisa de um email para autenticação
        "password": password
    })

    if "user" in response:
        user_id = response["user"]["id"]  # UUID gerado pelo Supabase

        # Agora inserimos os dados do usuário na tabela `users`
        supabase.table("users").insert({
            "id": user_id,
            "username": username,  # Corrigido: Agora usamos `username`
            "password": password,  # Supabase já armazena a senha na autenticação, então pode não ser necessário
            "user_type": user_type
        }).execute()
    
    return response

if __name__ == "__main__":
    main()
