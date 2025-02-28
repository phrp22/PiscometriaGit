import streamlit as st
from auth import get_user, sign_out
from layout import render_main_layout

# 🔧 Configuração inicial
st.set_page_config(
    page_title="Academia Diagnóstica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"  # Sidebar fechada no início
)

# 🌱 Inicializa sessão do usuário
if "user" not in st.session_state:
    st.session_state["user"] = None

if "show_sidebar" not in st.session_state:
    st.session_state["show_sidebar"] = False  # Sidebar começa fechada

def main():
    """Controla a execução do aplicativo."""
    
    user = get_user()
    
    # 🔐 Renderiza a sidebar apenas se necessário
    if st.session_state["show_sidebar"]:
        render_sidebar(user)

    # 🎨 Renderiza o layout principal
    render_main_layout()

    # 🔄 Atualiza a interface caso necessário
    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

if __name__ == "__main__":
    main()
