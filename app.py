import streamlit as st
from auth import get_user
from main_layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from user_profile import render_onboarding_questionnaire
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
        st.session_state["user"] = None  # O usuário é inicializado como não autenticado.
   
    # Se o processamento das páginas ainda não foi executado...
    if "processing" not in st.session_state:
        st.session_state["processing"] = False # É porque não há nada para ser processado.
   
    # Se a interface do aplicativo ainda não foi atualizada...
    if "refresh" not in st.session_state:
        st.session_state["refresh"] = False # Devemos aguardar alguma interação do usuário.


# 🧭 Função principal que tudo controla.
def main():
    
    initialize_session_state() # Inicializa a sessão.
    load_css() # Cria o visual.
    user = get_user()  # E verifica quem está navegando.

    # Se temos um ID logado na sessão...
    if user and "id" in user:
        user_id = user["id"]  # Guardamos o ID para ser utilizado no fluxo.

        # Busca as informações do perfil do usuário.
        user_profile = get_user_info(user_id, full_profile=True)
        
        # Busca quais usuários são profissionais.
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
                render_dashboard() # Renderiza o dashboard normal.

    # Entretanto, se ninguém está logado...
    else:
        render_main_layout()  # Renderizamos o layout principal.


# ⏯️ Executa o código, sem mais demora.
if __name__ == "__main__":
    main() # Chamando main() e começando a história!