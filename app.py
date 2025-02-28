# app.py
import streamlit as st
from auth import get_user
from profile import user_has_profile, render_onboarding_questionnaire
from dashboard import render_dashboard
from professional import is_professional_enabled, render_professional_dashboard
from layout import render_main_layout

def main():
    user = get_user()  # Pega do Supabase Auth
    if user:
        # Checa se o usuário já tem um perfil na user_profile
        if not user_has_profile(user["id"]):
            # Renderiza o questionário inicial para coletar gênero, data de nascimento, etc.
            render_onboarding_questionnaire(user["id"])
        else:
            # Se já tem perfil, verifica se é profissional ou não
            if is_professional_enabled(user["email"]):
                render_professional_dashboard(user)
            else:
                render_dashboard()
    else:
        # Se não estiver logado, exibe a tela de login/cadastro
        render_main_layout()

if __name__ == "__main__":
    main()
