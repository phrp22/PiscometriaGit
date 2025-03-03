import streamlit as st
import pathlib
from auth import sign_in, sign_up, reset_password

def load_css():
    """Carrega o CSS externo e aplica os estilos no Streamlit."""
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.html(f"<style>{css_content}</style>")  # Aplica o CSS corretamente

# Aplicar CSS uma única vez
load_css()

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    st.markdown("<h1>Abaeté 🌱</h1>", unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color: #FFA500; font-size: 28px;'>"
        "Sistema inteligente e adaptado ao novo paradigma dimensional dos transtornos mentais</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    ##### 💻 **Transforme a sua prática clínica com tecnologia avançada:**
    
    - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
    - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados em tempo real.
    - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
    - **Utilize nossas correções automatizadas** para garantir mais precisão na interpretação dos dados.
    - **Monitore a evolução longitudinalmente** observando padrões ao longo do tempo.
    
    🎯 **Tenha em mãos um sistema inteligente e baseado em evidências.**  
    🔍 **Eleve sua prática profissional e ofereça um acompanhamento mais eficaz e personalizado.**  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)

    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    display_name = None
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")

    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    action_key = "login_button" if option == "Login" else "signup_button"
    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"

    # Apenas um botão estilizado com CSS
    if st.markdown(
        f'<div class="st-key-auth-action"><button>{action_text}</button></div>',
        unsafe_allow_html=True
    ):
        if option == "Login":
            user, message = sign_in(email, password)
            if user:
                st.session_state["user"] = user
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(message)
        else:
            user, message = sign_up(email, password, confirm_password, display_name)
            if user:
                st.session_state["account_created"] = True
                st.success("📩 Um e-mail de verificação foi enviado para a sua caixa de entrada.")
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(message)

    if option == "Login":
        # Apenas um botão de recuperação de senha estilizado
        if st.markdown(
            '<div class="st-key-reset-password"><button>🔓 Recuperar Senha</button></div>',
            unsafe_allow_html=True
        ):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")
