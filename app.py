import streamlit as st
from auth import sign_in, sign_up, sign_out, get_user

# 🔧 Configuração inicial: modo escuro e sidebar fechada
st.set_page_config(
    page_title="Academia Diagnóstica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"  # Fecha a sidebar no início
)

# 🌱 Inicializa a sessão do usuário
if "user" not in st.session_state:
    st.session_state["user"] = None

if "show_sidebar" not in st.session_state:
    st.session_state["show_sidebar"] = False  # Sidebar começa fechada

def main():
    """Função principal do aplicativo."""
    
    # Obtém o usuário autenticado
    user = get_user()
    
    # 🔐 Sidebar de autenticação (abre automaticamente se `show_sidebar` for True)
    if st.session_state["show_sidebar"]:
        with st.sidebar:
            render_sidebar(user)

    # 🎨 Interface principal
    render_main_layout()

    # 🔄 Atualiza a interface caso necessário
    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

def render_sidebar(user):
    """Renderiza a sidebar de autenticação"""
    st.title("🔑 Autenticação")

    if user:
        st.write(f"👤 Usuário: {user['email']}")  
        if st.button("Sair", key="logout"):
            sign_out()
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
    else:
        auth_section()

def render_main_layout():
    """Renderiza a interface principal com título e botão de navegação."""
    
    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Criando um botão estilizado para abrir a sidebar
    col1, col2, col3 = st.columns([1, 3, 1])  # Layout centralizado

    with col2:  # Centraliza o botão
        button_html = """
        <style>
            .explore-button {
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
                display: inline-block;
            }
            .explore-button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
        </style>
        <script>
            function openSidebar() {
                var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.display = "block";
                }
            }
        </script>
        <button class="explore-button" onclick="openSidebar()">🚀 Explorar Agora</button>
        """
        st.markdown(button_html, unsafe_allow_html=True)

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

def auth_section():
    """Área de autenticação"""
    option = st.radio("Acesso", ["Login", "Cadastro"], key="auth_option")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if option == "Cadastro":
        confirm_password = st.text_input("Confirme a Senha", type="password")
        if st.button("Criar Conta"):
            user, message = sign_up(email, password, confirm_password)
            if user:
                st.success(message)
                st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            else:
                st.error(message)

    elif option == "Login":
        if st.button("Entrar"):
            user, message = sign_in(email, password)
            if user:
                st.success(message)
                st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            else:
                st.error(message)

if __name__ == "__main__":
    main()
