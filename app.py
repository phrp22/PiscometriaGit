import streamlit as st
from auth import get_user
from main_layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from profile import render_onboarding_questionnaire
from utils.design_utils import load_css
from utils.professional_utils import is_professional_enabled
from utils.user_utils import get_user_info

# Configuração inicial.
# Definimos título, ícone e o layout central.
st.set_page_config(
    page_title="Academia Diagnóstica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# 🌐 Função para inicializar a sessão e evitar erros de navegação.
def initialize_session_state():
    # Se a sessão ainda não estiver definida...
    if "user" not in st.session_state:
        st.session_state["user"] = None  # Definimos o usuário como não autenticado.
    # E se o processamento das páginas ainda não foi iniciado...
    if "processing" not in st.session_state:
        st.session_state["processing"] = False # É porque ainda não há nada para ser processado.


# 🧭 Função principal que tudo controla.
def main():
    initialize_session_state() # Estabelece os ponteiros onde tudo se desenrola.
    load_css() # E também cria o visual que é fundamental.
    user = get_user()  # Além de verificar quem está navegando. Retorna um dicionário com o ID do Supabse Auth, email e display_name do usuário.

    # Se temos um usuário com ID logado na sessão...
    if user and "id" in user:
        user_id = user["id"]  # Guardamos o ID para ser utilizado nas funções.

        # Busca as informações do perfil do usuário com todos os campos. Retorna um dicionário contendo os dados completos do usuário.
        user_profile = get_user_info(user_id, full_profile=True)
        # Busca quais usuários são profissionais. Retorna um dicionário com auth_user_id, email e area_habilitada do usuário.
        is_professional = is_professional_enabled(user_id)

        # Se o questionário de cadastro ainda não foi respondido...
        if not user_profile or not user_profile.get("genero"):
            render_onboarding_questionnaire(user_id, user["email"]) # Renderizamos o questionário de cadastro.

        # Mas...
        else:
            # Se o usuário é profissional...
            if is_professional:
                render_professional_dashboard(user) # Exibe um dashboard especial.
            # Caso contrário...
            else:
                render_dashboard() # Fica o dashboard normal.

    # Entretanto, se ninguém está logado...
    else:
        render_main_layout()  # Renderizamos o layout principal.


# ⏯️ Executa o código, sem mais demora.
if __name__ == "__main__":
    main() # Chamando main() e começando a história!
