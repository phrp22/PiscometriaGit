import streamlit as st
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com título e opções de Login e Cadastro."""

    st.title("Academia Diagnóstica 🧠")

    st.markdown(
        """
        ##### 💻 **Transforme a sua prática clínica com tecnologia avançada**  
        
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados e insights em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas**, garantindo precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente**, observando padrões de melhora ou agravamento ao longo do tempo.
        
        🎯 **Com a Academia Diagnóstica, você tem em mãos um sistema inteligente e baseado em evidências.**  
        
        🔍 **Eleve sua prática para um novo nível e ofereça aos seus pacientes um acompanhamento mais eficaz e personalizado.**  
        """
    )

    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    # Se for Cadastro, exibe os campos adicionais
    display_name = None
    confirm_password = None
    if option == "Cadastro":
        display_name = st.text_input("Nome", key="display_name_input")
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")

    action_text = "Entrar 🚀" if option == "Login" else "Criar Conta 📩"

    if st.button(action_text, key="auth_action"):
        if option == "Login":
            user, message = sign_in(email, password)
        else:
            user, message = sign_up(email, password, confirm_password, display_name)

        if user:
            st.session_state["user"] = user
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
