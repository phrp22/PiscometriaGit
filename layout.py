import streamlit as st
from auth import sign_in, sign_up, reset_password
from styles import BUTTON_STYLE, TITLE_STYLE  # supondo que você já tenha esses
# Caso queira usar a fonte global, importe também:
# from styles import GLOBAL_FONT_STYLE

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""
    
    # Se quiser mudar a fonte global:
    # st.markdown(GLOBAL_FONT_STYLE, unsafe_allow_html=True)

    # Se tiver um TITLE_STYLE, aplique:
    st.markdown(TITLE_STYLE, unsafe_allow_html=True)
    st.title("Academia Diagnóstica 🧠")

   st.markdown(
        """
        <div style="font-size:1.3rem; color:#FFA500; font-weight:bold; margin-bottom:10px;">
            💻 Transforme a sua prática clínica com tecnologia avançada
        </div>
        <ul>
            <li><strong>Crie uma conta profissional</strong> e acesse um ambiente especializado para profissionais da saúde mental.</li>
            <li><strong>Cadastre pacientes e acompanhe sua trajetória clínica</strong> com dados organizados em tempo real.</li>
            <li><strong>Aplique avaliações informatizadas</strong> e obtenha resultados rápidos e padronizados.</li>
            <li><strong>Utilize nossas correções automatizadas</strong> para garantir mais precisão na interpretação dos dados.</li>
            <li><strong>Monitore a evolução longitudinalmente</strong> observando padrões ao longo do tempo.</li>
        </ul>

        🎯 <strong>Tenha em mãos um sistema inteligente e baseado em evidências.</strong>  
        🔍 <strong>Eleve sua prática clínica e ofereça um acompanhamento mais eficaz e personalizado.</strong>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    display_name = None
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")

    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    action_text = "Entrar" if option == "Login" else "Criar Conta"

    if option == "Cadastro" and st.session_state.get("account_created", False):
        st.info("📩 Um e-mail de verificação foi enviado para a sua caixa de entrada.")
    else:
        if st.button(action_text, key="auth_action"):
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
        if st.button("Recuperar Senha"):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")
