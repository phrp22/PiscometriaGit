import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

import pathlib
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile

def load_css():
    """Carrega o CSS externo e aplica os estilos no Streamlit."""
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.html(f"<style>{css_content}</style>")  # Agora usando `st.html()` corretamente

# Aplicar CSS uma única vez
load_css()

# Inicializa a sessão do usuário, se ainda não estiver definida
if "user" not in st.session_state:
    st.session_state["user"] = None

# Função principal do aplicativo
def main():
    user = get_user()  # Obtém as informações do usuário autenticado
    
    if user:
        if not user_has_profile(user["id"]):
            render_onboarding_questionnaire(user["id"], user["email"])
        else:
            if is_professional_enabled(user["id"]):
                render_professional_dashboard(user)
            else:
                render_dashboard()
    else:
        render_main_layout()

# Executa a aplicação
if __name__ == "__main__":
    main()