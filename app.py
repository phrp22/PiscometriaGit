import streamlit as st 
import pathlib

# Configuração da página para um visual legal.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Importações já existentes.
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile

# --- Novas importações para o Supabase ---
from supabase import create_client, Client

# Configurações do Supabase (certifique-se de que as chaves estão em st.secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Carrega o CSS para estilizar o visual, aplicando no Streamlit um design mais legal.
def load_css():
    css_path = pathlib.Path("assets/styles.css")  # Caminho do código de estilo.
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.html(f"<style>{css_content}</style>")

# Função para inicializar a sessão e evitar erro na navegação.
def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None

# Função para atualizar a senha do usuário utilizando o token de recuperação.
def update_user_password(token, new_password):
    """
    Utiliza o token recebido (do link de recuperação) para atualizar a senha do usuário.
    """
    response = supabase.auth.api.update_user(token, {"password": new_password})
    return response

# Função para renderizar a página de recuperação de senha.
def render_password_recovery(token):
    st.subheader("Redefinir Senha")
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Nova Senha", type="password")
    if st.button("Atualizar Senha"):
        if not new_password:
            st.error("A senha não pode ser vazia!")
        elif new_password != confirm_password:
            st.error("As senhas não conferem!")
        else:
            result = update_user_password(token, new_password)
            if result.get("error"):
                st.error(f"Erro ao atualizar senha: {result['error']}")
            else:
                st.success("Senha atualizada com sucesso! Faça login com sua nova senha.")

# Função principal que controla o fluxo do app.
def main():
    initialize_session_state()
    load_css()
    
    # Tenta utilizar st.get_query_params(); se não existir, utiliza st.experimental_get_query_params()
    try:
        query_params = st.get_query_params()
    except AttributeError:
        query_params = st.experimental_get_query_params()
    
    if "token" in query_params and query_params.get("type", [""])[0] == "recovery":
         token = query_params["token"][0]
         render_password_recovery(token)
         return  # Interrompe a execução para não renderizar outras páginas

    user = get_user()
    if user and isinstance(user, dict) and "id" in user:
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
        render_main_layout()  # Tela inicial.

if __name__ == "__main__":
    main()
