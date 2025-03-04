import streamlit as st
import streamlit.components.v1 as components
from auth import sign_in, sign_up, reset_password


def disable_autofill():
    """
    Injeta JavaScript para desativar o preenchimento automático nos campos de email e senha.
    """
    components.html(
        """
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            setTimeout(function() {
                let emailField = document.querySelector('input[type="email"]');
                let passwordField = document.querySelector('input[type="password"]');

                if (emailField) {
                    emailField.setAttribute("autocomplete", "new-email");
                    emailField.setAttribute("name", "email_disable_autofill");
                    emailField.value = "";
                }

                if (passwordField) {
                    passwordField.setAttribute("autocomplete", "new-password");
                    passwordField.setAttribute("name", "password_disable_autofill");
                    passwordField.value = "";
                }
            }, 500);
        });
        </script>
        """,
        height=0,
        width=0
    )


def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    st.markdown("# Abaeté 🌱")

    # Texto estilizado
    st.markdown(
        """
        <h1 style='color: #FFA500; font-size: 28px; font-weight: bold;'>
        Um sistema inteligente que cuida de você!</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ##### 💻 **Transforme a sua prática clínica com tecnologia avançada:**
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas** para garantir mais precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente** observando padrões ao longo do tempo.
        🎯 **Tenha em mãos um sistema inteligente e baseado em evidências.**  
        🔍 **Eleve sua prática profissional e ofereça um acompanhamento mais eficaz e personalizado.**  
        """
    )

    st.divider()

    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    # Desativa o preenchimento automático
    disable_autofill()

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    display_name = None
    confirm_password = None

    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")

    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"

    if st.button(action_text, key="authaction", use_container_width=True):
        if not email or not password:
            st.warning("⚠️ O preenchimento automático foi desabilitado por motivos de segurança. Por favor, preencha todos os campos antes de continuar.")
        else:
            # Evita que a ação ocorra mais de uma vez por clique
            if "login_attempt" not in st.session_state:
                st.session_state["login_attempt"] = True

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

            # Remove a flag para evitar bloqueios na próxima tentativa
            st.session_state.pop("login_attempt", None)


    if option == "Login":
        if st.button("🔓 Recuperar Senha", key="resetpassword", use_container_width=True):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")
