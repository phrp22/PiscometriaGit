import streamlit as st
from auth import sign_in

def render_main_layout():
    """Renderiza a interface principal com título e login na parte inferior."""

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

    # 🔻 Login na parte inferior
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>🔑 Faça seu Login</h3>", unsafe_allow_html=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    login_button_html = f"""
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
    <form action="" method="POST">
        <input type="hidden" name="email" value="{email}">
        <input type="hidden" name="password" value="{password}">
        <button class="green-button" type="submit">🚀 Entrar</button>
    </form>
    """
    st.markdown(login_button_html, unsafe_allow_html=True)

    # Capturar o clique e processar login
    if "email_input" in st.session_state and "password_input" in st.session_state:
        email = st.session_state["email_input"]
        password = st.session_state["password_input"]
        if email and password:  # Se os campos estiverem preenchidos
            user, message = sign_in(email, password)
            if user:
                st.session_state["user"] = user
                st.success("✅ Login realizado com sucesso!")
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(message)
