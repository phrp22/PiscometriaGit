import streamlit as st
import pathlib
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    st.markdown("# Abaeté 🌱")

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
        display_name = st.text_input("Primeiro Nome", key="display_name_input")

    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"

    message_placeholder = st.empty()  # Espaço reservado para mensagens

    # **Exibe mensagens armazenadas antes de interações do usuário**
    if "error_message" in st.session_state:
        message_placeholder.error(st.session_state["error_message"])
        del st.session_state["error_message"]  # Remove erro para evitar duplicação

    if "confirmation_message" in st.session_state:
        message_placeholder.success(st.session_state["confirmation_message"])
        del st.session_state["confirmation_message"]  # Remove sucesso para evitar repetição

    # **Botão para Login/Cadastro**
    if st.button(action_text, key="authaction", use_container_width=True):
        if not email or not password:
            st.session_state["error_message"] = "⚠️ O preenchimento automático foi desabilitado por motivos de segurança. Preencha todos os campos antes de continuar."
            st.rerun()
        else:
            if option == "Login":
                user, message = sign_in(email, password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["refresh"] = True
                    st.rerun()
                else:
                    # **Se um erro já existe, evita sobrescrever**
                    if "error_message" not in st.session_state:
                        st.session_state["error_message"] = f"❌ Erro ao logar: {message}"
                    st.rerun()
            else:
                if not display_name or not confirm_password:
                    st.session_state["error_message"] = "⚠️ Todos os campos são obrigatórios. Preencha corretamente antes de continuar."
                    st.rerun()
                elif password != confirm_password:
                    st.session_state["error_message"] = "❌ As senhas não coincidem. Tente novamente."
                    st.rerun()
                else:
                    user, message = sign_up(email, password, confirm_password, display_name)
                    if user:
                        st.session_state["account_created"] = True
                        st.session_state["confirmation_message"] = "📩 Um e-mail de verificação foi enviado para a sua caixa de entrada."
                        st.rerun()
                    else:
                        st.session_state["error_message"] = message
                        st.rerun()

    # **Botão para recuperação de senha**
    if option == "Login":
        if st.button("🔓 Recuperar Senha", key="resetpassword", use_container_width=True):
            if email:
                message = reset_password(email)
                st.session_state["confirmation_message"] = message
                st.rerun()
            else:
                st.session_state["error_message"] = "⚠️ Por favor, insira seu email antes de redefinir a senha."
                st.rerun()