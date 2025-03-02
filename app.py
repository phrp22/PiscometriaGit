import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard
from professional import is_professional_enabled, render_professional_dashboard
from profile import get_user_profile, render_onboarding_questionnaire
from styles import BUTTON_STYLE

st.set_page_config(
    page_title="Academia Diagnóstica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Aplica os estilos globais uma única vez
st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    user = get_user()
    if user:
        # Verifica se o usuário já completou o onboarding (perfil criado)
        profile = get_user_profile(user["id"])
        if not profile:
            # Se não existir, exibe o questionário de onboarding
            render_onboarding_questionnaire(user["id"])
            return  # Após o onboarding, o app será recarregado (st.rerun())
        else:
            # Se o perfil existir, prossegue para a dashboard
            render_dashboard()
    else:
        render_main_layout()

if __name__ == "__main__":
    main()
