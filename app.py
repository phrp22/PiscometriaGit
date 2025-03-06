import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
from utils.helpers import load_css


# Configuração inicial.
# Definimos título, ícone e o layout central.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🪴",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# 🌐 Função para inicializar a sessão e evitar erros de navegação.
def initialize_session_state():
    # Se a sessão ainda não estiver definida...
    if "user" not in st.session_state:
        st.session_state["user"] = None  # Define o usuário como não autenticado.
    # Se o processamento das páginas ainda não foi iniciado...
    if "processing" not in st.session_state:
        st.session_state["processing"] = False # É porque ainda não temos nada para ser processado.

# Função principal que tudo controla.
# Definindo qual parte do app se desenrola.
def main():
    initialize_session_state() # O estado da sessão em primeiro lugar. 
    load_css() # Depois o visual, sem desandar. 
    user = get_user()  # Agora é a vez do usuário

    # Se temos um usuário logado na sessão...
    if user and "id" in user:
        user_id = user["id"]  # Guardamos o ID para evitar reuso desnecessário.

        # Buscamos as informações do perfil **apenas uma vez**!
        user_profile = get_user_profile(user_id)
        is_professional = is_professional_enabled(user_id)

        # Se o questionário inicial ainda não foi preenchido...
        if not user_profile:
            render_onboarding_questionnaire(user_id, user["email"])  # Coletamos dados para configurar o painel.
        else:
            # Se é profissional, exibir o dashboard especial.
            if is_professional:
                render_professional_dashboard(user)
            else:
                render_dashboard()  # Caso contrário, o dashboard normal!

    # Mas se ninguém está logado...
    else:
        render_main_layout()  # A tela inicial será mostrada.


# Executa o código, sem mais demora,
# Chamando main() e começando a história!
if __name__ == "__main__":
    main()