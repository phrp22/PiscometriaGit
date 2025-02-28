import streamlit as st
from auth import sign_in, sign_up, reset_password
from styles import BUTTON_STYLE, TITLE_STYLE  # Importando estilos

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""
    
    # Aplica o efeito mágico no título
    st.markdown(TITLE_STYLE, unsafe_allow_html=True)
    st.title("Academia Diagnóstica 🧠")  # O título original permanece

    st.markdown(
        """
        ##### 💻 **Transforme a sua prática clínica com tecnologia avançada.**  
        
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas** para garantir mais precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente** observando padrões ao longo do tempo.
        
        🎯 **Tenha em mãos um sistema inteligente e baseado em evidências.**  
        
        🔍 **Eleve sua prática clínica e ofereça um acompanhamento mais eficaz e personalizado.**  
        """
    )
    
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    # Alternador entre Login e Cadastro
    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)
    
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")
    
    # Se for Cadastro, exibe os campos adicionais para nome e confirmação de senha
    display_name = None
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")
        
    # 📌 Aplica estilo ao botão
    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)
    
    # Se o usuário alterna para Login, reseta a flag de conta criada
    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]
    
    # Define o texto do botão conforme a opção
    action_text = "🔮 Entrar" if option == "Login" else "🪄 Criar Conta"
    
    # Se estiver em Cadastro e a conta já foi criada, exibe a mensagem de verificação
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
                # Cadastro: cria a conta, mas NÃO loga o usuário automaticamente
                user, message = sign_up(email, password, confirm_password, display_name)
                if user:
                    st.session_state["account_created"] = True  # Suspende o botão de cadastro
                    st.success("📩 Um e-mail de verificação foi enviado para a sua caixa de entrada.")
                    st.session_state["refresh"] = True
                    st.rerun()
                else:
                    st.error(message)
    
    # Botão "Esqueci minha senha" aparece somente no Login
    if option == "Login":
        if st.button("🔓 Recuperar Senha"):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")
