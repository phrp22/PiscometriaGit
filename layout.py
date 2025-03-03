import streamlit as st
from auth import sign_in, sign_up, reset_password  # Importa as funções de autenticação
import pathlib

# 🔹 Função para carregar CSS externo com `st.html()`
def load_css():
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.html(f"<style>{css_content}</style>")  # 🔥 Agora usando `st.html()`

# Aplica CSS uma única vez
load_css()

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    # 🔹 Título principal alinhado à esquerda
    st.markdown(
        "<h1 style='text-align: left; color: white;'>Abaeté 🌱</h1>",
        unsafe_allow_html=True
    )

    # 🔹 Frase de destaque em laranja
    st.markdown(
        "<h2 style='text-align: left; color: #FFA500; font-size: 28px;'>"
        "Sistema inteligente e adaptado ao novo paradigma dimensional dos transtornos mentais</h2>",
        unsafe_allow_html=True
    )

    # 🔹 Descrição do sistema
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

    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    # 🔹 Alternador entre Login e Cadastro
    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)
    
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")
    
    # 🔹 Campos adicionais para Cadastro
    display_name = None
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")
    
    # 🔹 Resetar flag se mudar para Login
    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]
    
    # 🔹 Define o texto do botão conforme a opção
    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"
    
    # 🔹 Mensagem de conta criada
    if option == "Cadastro" and st.session_state.get("account_created", False):
        st.info("📩 Um e-mail de verificação foi enviado para a sua caixa de entrada.")
    else:
        # 🔹 Botão de ação com estilo roxo (`st-key-primary`)
        if st.button(action_text, key="primary-auth"):
            if option == "Login":
                user, message = sign_in(email, password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["refresh"] = True
                    st.rerun()
                else:
                    st.error(message)
            else:
                # 🔹 Cadastro: cria a conta, mas NÃO loga automaticamente
                user, message = sign_up(email, password, confirm_password, display_name)
                if user:
                    st.session_state["account_created"] = True
                    st.success("📩 Um e-mail de verificação foi enviado para a sua caixa de entrada.")
                    st.session_state["refresh"] = True
                    st.rerun()
                else:
                    st.error(message)
    
    # 🔹 Botão "Esqueci minha senha" aparece somente no Login
    if option == "Login":
        if st.button("🔓 Recuperar Senha", key="primary-reset-password"):
            if email:
                message = reset_password(email)
                st.info(message)
            else:
                st.warning("⚠️ Por favor, insira seu email antes de redefinir a senha.")