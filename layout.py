import streamlit as st
from auth import sign_in, sign_up

def render_main_layout():
    """Renderiza a interface principal com título e opções de Login e Cadastro na parte inferior."""

    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Introdução com Markdown
    st.markdown(
        """
        #### **Como a Academia Diagnóstica pode transformar sua prática?**  
        
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

    # 📌 Botão estilizado para Login/Cadastro
    action_text = "🚀 Entrar" if option == "Login" else "📩 Criar Conta"
    button_html = f"""
    <style>
        .green-button {{
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
            width: 100%;
            text-align: center;
            display: block;
            margin-top: 10px;
        }}
        .green-button:hover {{
            background-color: #45a049;
            transform: scale(1.05);
        }}
    </style>
    <button class="green-button" onclick="document.getElementById('auth_action').click()">{action_text}</button>
    """
    st.markdown(button_html, unsafe_allow_html=True)

    # 📌 Captura do clique e execução da autenticação
    if st.button(action_text, key="auth_action", help="Clique no botão verde acima para continuar"):
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
