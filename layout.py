import streamlit as st
import pathlib
from auth import sign_in, sign_up, reset_password


def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    st.markdown("# Abaeté 🌱")

    # Texto laranja estilizado e aumentado para maior destaque
    st.markdown(
        """
        <h1 style='color: #FFA500; font-size: 28px; font-weight: bold;'>
        Um sistema inteligente que cuida de você!</h1>
        """,
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

    st.divider()

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

    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"

    # Botão estilizado com a classe do CSS
    if st.button(action_text, key="authaction", use_container_width=True):
        if option == "Login":
            user, message = sign_in(email, password)
            if user:
                st.session_state["user"] = user
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(f"❌ Erro ao logar: {message}")
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
        if st.button("🔓 Recuperar Senha", key="resetpassword", use_container_width=True):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")
