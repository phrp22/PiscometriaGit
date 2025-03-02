# app.py
import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
from styles import DARK_THEME_STYLE
 # <-- Importa o tema escuro

st.set_page_config(
    page_title="PsyTrack",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Aplica o tema escuro (fundo, texto branco, sidebar etc.)
st.markdown(DARK_THEME_STYLE, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    user = get_user()
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

if __name__ == "__main__":
    main()
