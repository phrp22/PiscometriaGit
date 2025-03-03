import streamlit as st

st.set_page_config(
    page_title="PsyTrack",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
from styles import BUTTON_STYLE, ACCEPT_BUTTON_STYLE, REJECT_BUTTON_STYLE

# Aplica os estilos globais uma única vez
st.markdown(BUTTON_STYLE, unsafe_allow_html=True)
st.markdown(ACCEPT_BUTTON_STYLE, unsafe_allow_html=True)
st.markdown(REJECT_BUTTON_STYLE, unsafe_allow_html=True)


if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    user = get_user()  # Obtém as informações do usuário autenticado
    if user:
        # Primeiro verifica se o usuário tem um perfil
        if not user_has_profile(user["id"]):
            render_onboarding_questionnaire(user["id"], user["email"])
        else:
            # Se ele for um profissional habilitado, mostra a dashboard profissional
            if is_professional_enabled(user["id"]):
                render_professional_dashboard(user)
            else:
                render_dashboard()  # Caso contrário, mostra a dashboard padrão (para pacientes)
    else:
        render_main_layout()

if __name__ == "__main__":
    main()