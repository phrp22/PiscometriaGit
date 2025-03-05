import streamlit as st 

# Configuração da página para um visual legal.
# Definimos título, ícone e layout central.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

import pathlib
import os
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire

# 📌 Captura os parâmetros da URL corretamente
query_params = st.query_params
route = query_params.get("route")

# 🔄 Se a URL for /reset-password, redireciona usando JavaScript
if route == "reset-password":
    st.markdown(
        """
        <script>
            window.location.replace("/#reset-password");
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.stop()  # Impede o restante do código de rodar

# Carrega o CSS para estilizar o visual, aplicando no Streamlit um design mais legal.
def load_css():
    css_path = pathlib.Path("assets/styles.css")  # Caminho do código de estilo.
    if css_path.exists():
        with open(css_path, "r") as f:  # Abrimos o código para leitura.
            css_content = f.read()  # Pegamos o conteúdo e guardamos para consulta.
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)  # Aplicamos o estilo na tela!

# Função para inicializar a sessão e evitar erro na navegação.
def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None  # Define o usuário como não autenticado.

# Função principal que tudo controla.
def main():
    initialize_session_state()  # Inicializa a sessão antes de tudo.
    load_css()  # Aplica o CSS para manter o visual bonito.

    user = get_user()  # Obtém os dados do usuário autenticado.

    if user and "id" in user:
        user_id = user["id"]
        user_profile = get_user_profile(user_id)
        is_professional = is_professional_enabled(user_id)

        if not user_profile:
            render_onboarding_questionnaire(user_id, user["email"])
        else:
            if is_professional:
                render_professional_dashboard(user)
            else:
                render_dashboard()
    else:
        render_main_layout()  # Mostra a tela inicial.

# Executa o código principal
if __name__ == "__main__":
    if st.query_params.get("route") == "reset-password":
        from reset_password import reset_password_page
        reset_password_page()
        st.stop()
    else:
        main()
