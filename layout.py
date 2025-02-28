import streamlit as st
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com título e opções de Login e Cadastro na parte inferior."""

    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Introdução com Markdown
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

    # 🔻 Login/Cadastro na parte inferior
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>🔑 Acesse sua Conta</h3>", unsafe_allow_html=True)

    # 📌 Alternador entre Login e Cadastro
    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    # 📌 Se for Cadastro, exibir confirmação de senha
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")

    # 📌 Estilizar o botão com CSS para ficar verde
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

    # 📌 Botão real do Streamlit (único)
    action_text = "🚀 Entrar" if option == "Login" else "📩 Criar Conta"
    if st.button(action_text, key="auth_action"):
        if option == "Login":
            user, message = sign_in(email, password)
        else:
            user, message = sign_up(email, password, confirm_password)

        if user:
            st.session_state["user"] = user
            st.success("✅ Autenticação realizada com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()
        else:
            st.error(message)

    # 📌 Botão "Esqueci minha senha"
    if option == "Login":
        if st.button("🔑 Esqueci minha senha"):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("Por favor, insira seu email antes de redefinir a senha.")
