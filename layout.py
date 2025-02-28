import streamlit as st
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com título e opções de Login e Cadastro na parte inferior."""

    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📝 Aqui trazemos a explicação,  
    # De como usar essa inovação!  
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

    # 🔻 Aqui o Login e Cadastro vão se encontrar,  
    # Só escolher qual você quer usar!  
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    # 🔄 Alternância entre Login e Cadastro  
    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    # ✉️ Digite seu email, sem hesitar,  
    email = st.text_input("Email", key="email_input")

    # 🔐 Sua senha agora vamos guardar!  
    password = st.text_input("Senha", type="password", key="password_input")

    # 📌 Se for Cadastro, há algo a mais,  
    # Precisamos confirmar a senha, sem sinais!  
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")

    # 🎨 Um botão bonito, pra ficar sensacional,  
    # Verde, elegante, um toque especial!  
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

    # 🛠️ Se mudar para Login, vamos ajeitar,  
    # O aviso de conta criada precisa apagar!  
    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    # 🔘 O botão com ação especial,  
    action_text = "Entrar 🚀" if option == "Login" else "📩 Criar Conta"

    # 📩 Se a conta foi criada, não há mais ação,  
    # Só mostramos um aviso, sem preocupação!  
    if option == "Cadastro" and st.session_state.get("account_created", False):
        st.info("📩 Um e-mail de verificação foi enviado. Confirme para acessar sua conta.")
    else:
        # 🎯 Aqui vem a lógica, simples e sagaz,  
        if st.button(action_text, key="auth_action"):
            if option == "Login":
                user, message = sign_in(email, password)
            else:
                user, message = sign_up(email, password, confirm_password)

            # 🎉 Se tudo der certo, é hora de vibrar,  
            if user:
                st.session_state["user"] = user
                if option == "Cadastro":
                    st.session_state["account_created"] = True  # Suspende o botão
                st.success("✅ Autenticação realizada com sucesso!" if option == "Login" else "📩 Um e-mail de verificação foi enviado. Confirme para acessar sua conta.")
                st.session_state["refresh"] = True
                st.rerun()
            else:
                st.error(message)  # 🚨 Se algo falhou, vamos avisar!

    # 🔑 Se a senha sumiu da sua mente,  
    # Não se preocupe, tem um jeito excelente!  
    if option == "Login":
        if st.button("Esqueci minha senha"):
            if email:
                message = reset_password(email)
                st.info(message)  # 📩 Um email será enviado rapidinho!
            else:
                st.warning("Por favor, insira seu email antes de redefinir a senha.")  # ⚠️ Não podemos adivinhar!
