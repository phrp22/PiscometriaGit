import streamlit as st
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""
    
    st.title("Academia Diagnóstica 🧠")
    st.markdown("##### 💻 **Transforme a sua prática clínica com tecnologia avançada**")
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)
    
    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")
    
    display_name = None
    confirm_password = None
    if option == "Cadastro":
        display_name = st.text_input("Nome", key="display_name_input")
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")

    st.markdown(
        """
        <style>
            div.stButton > button:first-child {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.3s;
                width: 100%;
                padding: 12px 24px;
                text-align: center;
            }
            div.stButton > button:first-child:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
        </style>
        """, unsafe_allow_html=True
    )
    
    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    action_text = "Entrar 🚀" if option == "Login" else "Criar Conta 📩"
    
    if option == "Cadastro" and st.session_state.get("account_created", False):
        st.info("📩 Um e-mail de verificação foi enviado. Confirme para acessar sua conta.")
    else:
        if st.button(action_text, key="auth_action"):
            if option == "Login":
                user, message = sign_in(email, password)
            else:
                user, message = sign_up(email, password, confirm_password, display_name)
            
            if user:
                st.session_state["user"] = user
                if option == "Cadastro":
                    st.session_state["account_created"] = True
                st.success("✅ Autenticação realizada com sucesso!" if option == "Login" else "📩 Um e-mail de verificação foi enviado. Confirme para acessar sua conta.")
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(message)
    
    if option == "Login":
        if st.button("Esqueci minha senha"):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("Por favor, insira seu email antes de redefinir a senha.")
