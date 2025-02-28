import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard

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

def main():
    """Controla a execução do aplicativo."""
    
    user = get_user()
    
    if user:
        render_dashboard()  # 🚀 Se o usuário está logado, mostramos o dashboard
    else:
        render_main_layout()  # 🏠 Se não está logado, mostramos a tela inicial

    # 🔄 Atualiza a interface caso necessário
    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

if __name__ == "__main__":
    main()
