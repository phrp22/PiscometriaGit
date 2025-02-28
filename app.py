import streamlit as st
from auth import sign_in, sign_up, sign_out, get_user

# 🔧 Configuração inicial da página
st.set_page_config(page_title="Academia Diagnóstica", page_icon="🧠", layout="centered")

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

    # 🎨 Interface principal
    render_main_layout()

    # 🔄 Atualiza a interface caso necessário
    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

def render_main_layout():
    """Renderiza a interface principal com título e botão de navegação."""
    
    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Criando um botão interativo para explorar a plataforma
    col1, col2, col3 = st.columns([1, 3, 1])  # Cria um layout centralizado

    with col2:  # Centraliza o botão
        if st.button("**Transforme sua prática clínica com tecnologia avançada** 💡", use_container_width=True):
            # Simula a abertura da sidebar em dispositivos móveis
            st.session_state["show_sidebar"] = not st.session_state.get("show_sidebar", False)

    # 📌 Introdução com Markdown
    st.markdown(
        """
        #### **Benefícios**  
        
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados e insights em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas**, garantindo precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente**, observando padrões de melhora ou agravamento ao longo do tempo.

        🎯 **Com a Academia Diagnóstica, você tem em mãos um sistema inteligente e baseado em evidências.**  
        
        🔍 **Eleve sua prática clínica e ofereça aos seus pacientes um acompanhamento mais eficaz e personalizado.**  
        """
    )

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

