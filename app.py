import locale

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')

import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard
from professional import is_professional_enabled, render_professional_dashboard
from styles import BUTTON_STYLE
from profile import user_has_profile, render_onboarding_questionnaire

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
    user = get_user()  # Tenta obter o usuário autenticado
    if user:
        # Se o usuário estiver logado, então verifica se já possui um perfil
        if not user_has_profile(user["id"]):
            render_onboarding_questionnaire(user["id"])
        else:
            # Se já tiver perfil, exibe o dashboard ou outra tela principal
            render_dashboard()
    else:
        # Se não estiver logado, exibe a tela de login/cadastro
        render_main_layout()


if __name__ == "__main__":
    main()