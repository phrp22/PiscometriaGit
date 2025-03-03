import streamlit as st
from streamlit_extras.st_html import st_html
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
from styles import BUTTON_STYLE, ACCEPT_BUTTON_STYLE, REJECT_BUTTON_STYLE

# Configuração da página
st.set_page_config(
    page_title="Abaeté",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Função para carregar o CSS utilizando a extensão
def load_css():
    if "css_loaded" not in st.session_state:
        st_html(BUTTON_STYLE)
        st_html(ACCEPT_BUTTON_STYLE)
        st_html(REJECT_BUTTON_STYLE)
        st.session_state["css_loaded"] = True  # Define flag para evitar múltiplos carregamentos

# Executa o carregamento do CSS
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
