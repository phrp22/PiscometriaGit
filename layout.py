import streamlit as st
from auth import sign_in, sign_up, reset_password

def render_main_layout():
    """Renderiza a interface principal com opções de Login e Cadastro."""

    # Força a aplicação do CSS carregado no app.py
    st.html("<div></div>")  # Garante que o CSS já foi carregado

    st.markdown("# Abaeté 🌱")
    st.markdown("## 🌟 Sistema inteligente e adaptado ao novo paradigma dimensional dos transtornos mentais")

    st.markdown("""
    ##### 💻 **Transforme a sua prática clínica com tecnologia avançada:**
    
    - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
    - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados em tempo real.
    - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
    - **Utilize nossas correções automatizadas** para garantir mais precisão na interpretação dos dados.
    - **Monitore a evolução longitudinalmente** observando padrões ao longo do tempo.
    
    🎯 **Tenha em mãos um sistema inteligente e baseado em evidências.**  
    🔍 **Eleve sua prática profissional e ofereça um acompanhamento mais eficaz e personalizado.**  
    """)

    st.divider()

    option = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Senha", type="password", key="password_input")

    display_name = None
    confirm_password = None
    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_password_input")
        display_name = st.text_input("Nome", key="display_name_input")

    if option == "Login" and "account_created" in st.session_state:
        del st.session_state["account_created"]

    action_text = "Entrar" if option == "Login" else "🪄 Criar Conta"

    # Renderiza o botão estilizado pelo CSS (sem `st.button()`)
    st.html(f"""
    <div class="st-key-auth-action">
        <button id="auth_button">{action_text}</button>
    </div>
    """)

    # Captura evento do botão via JavaScript
    st.html("""
    <script>
        document.getElementById('auth_button').onclick = function() {
            parent.window.streamlitRerun();
        };
    </script>
    """)

    # Lógica de login e cadastro
    if "clicked_auth" in st.session_state and st.session_state["clicked_auth"]:
        st.session_state["clicked_auth"] = False  # Reseta estado do botão

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

    if option == "Login":
        # Renderiza o
