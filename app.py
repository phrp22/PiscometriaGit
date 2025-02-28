import streamlit as st
from auth import sign_in, sign_up, sign_out, get_user

# 🔧 Configuração inicial da página
st.set_page_config(page_title="PsyTrack Beta", page_icon="📊", layout="centered")

# 🌱 Inicializa a sessão do usuário
if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    """Função principal do aplicativo."""
    
    # Obtém o usuário autenticado
    user = get_user()
    
    # 🔐 Barra lateral para autenticação
    st.sidebar.title("🔑 Autenticação")

    if user:
        st.sidebar.write(f"👤 Usuário: {user['email']}")  

        # 🚪 Botão de logout
        if st.sidebar.button("Sair"):
            sign_out()
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar

    else:
        auth_section()

    # 📊 Nome do app na tela principal
    st.title("📊 PsyTrack Beta - Gestão de Dados")

    # 🔄 Atualiza a interface caso necessário
    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

def auth_section():
    """Área de autenticação"""
    option = st.sidebar.radio("Acesso", ["Login", "Cadastro"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Senha", type="password")

    if option == "Cadastro":
        confirm_password = st.sidebar.text_input("Confirme a Senha", type="password")
        if st.sidebar.button("Criar Conta"):
            user, message = sign_up(email, password, confirm_password)
            if user:
                st.sidebar.success(message)
                st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            else:
                st.sidebar.error(message)

    elif option == "Login":
        if st.sidebar.button("Entrar"):
            user, message = sign_in(email, password)
            if user:
                st.sidebar.success(message)
                st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            else:
                st.sidebar.error(message)

if __name__ == "__main__":
    main()
