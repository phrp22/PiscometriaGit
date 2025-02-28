import streamlit as st
from auth import sign_in, sign_up, sign_out

def render_sidebar(user):
    """Renderiza a sidebar de autenticação."""
    st.sidebar.title("🔑 Autenticação")

    if user:
        st.sidebar.write(f"👤 Usuário: {user['email']}")
        if st.sidebar.button("Sair", key="logout"):
            sign_out()
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
    else:
        auth_section()

def auth_section():
    """Área de autenticação na sidebar."""
    option = st.sidebar.radio("Acesso", ["Login", "Cadastro"], key="auth_option")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Senha", type="password")

    if option == "Cadastro":
        confirm_password = st.sidebar.text_input("Confirme a Senha", type="password")
        if st.sidebar.button("Criar Conta"):
            user, message = sign_up(email, password, confirm_password)
            if user:
                st.sidebar.success(message)
                st.session_state["refresh"] = True
            else:
                st.sidebar.error(message)

    elif option == "Login":
        if st.sidebar.button("Entrar"):
            user, message = sign_in(email, password)
            if user:
                st.sidebar.success(message)
                st.session_state["refresh"] = True
            else:
                st.sidebar.error(message)
