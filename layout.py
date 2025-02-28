import streamlit as st

def render_main_layout():
    """Renderiza a interface principal com título e login na tela principal."""

    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Criando a área de login no centro
    col1, col2, col3 = st.columns([1, 3, 1])  # Layout centralizado

    with col2:  # Centraliza o login
        st.markdown("<h3 style='text-align: center;'>🔑 Faça seu Login</h3>", unsafe_allow_html=True)

        email = st.text_input("Email", key="email_input")
        password = st.text_input("Senha", type="password", key="password_input")

        login_button = """
        <style>
            .green-button {
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
            }
            .green-button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
        </style>
        <button class="green-button" onclick="document.getElementById('login_action').click()">🚀 Entrar</button>
        """
        st.markdown(login_button, unsafe_allow_html=True)

        # Botão invisível para capturar clique do HTML
        if st.button("Entrar", key="login_action", help="Clique no botão verde acima para logar"):
            st.session_state["auth_trigger"] = True  # Ativa autenticação
            st.rerun()  # Recarrega a interface

    # 📌 Introdução com Markdown
    st.markdown(
        """
        ##### **Transforme a sua prática clínica com tecnologia avançada** 
        
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas**, garantindo precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente**, observando padrões de melhora ou agravamento ao longo do tempo.

        🎯  **Com a Academia Diagnóstica, você tem em mãos um sistema inteligente e baseado em evidências.**  
        
        🔍  **Eleve sua prática para um novo nível e ofereça aos seus pacientes um acompanhamento mais eficaz e personalizado.**  
        """
    )
