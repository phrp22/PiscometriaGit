import streamlit as st
import pathlib
from auth import sign_in, sign_up, reset_password, update_user_password, sign_out, get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire

# Configuração da página para um visual legal.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Script para mover os parâmetros do fragmento (#) para a query string
st.markdown(
    """
    <script>
    (function() {
        var hash = window.location.hash;
        if (hash && hash.length > 1) {
            hash = hash.substring(1); // remove o "#"
            var currentQuery = window.location.search;
            if (currentQuery) {
                // Combina os parâmetros existentes com os do fragmento
                currentQuery = currentQuery + '&' + hash;
            } else {
                currentQuery = '?' + hash;
            }
            var newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + currentQuery;
            window.history.replaceState(null, null, newUrl);
        }
    })();
    </script>
    """,
    unsafe_allow_html=True
)


# Função para carregar o CSS customizado (NÃO ALTERAR)
def load_css():
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.html(f"<style>{css_content}</style>")  # NÃO ALTERAR esta linha!

# Função para inicializar a sessão
def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None

# Função para tratar o fluxo de redefinição de senha
def handle_password_reset():
    """Verifica a URL por parâmetros de redefinição de senha e exibe um formulário."""
    query_params = st.query_params
    # Tenta obter 'token' ou 'access_token'
    token = query_params.get("token") or query_params.get("access_token")
    recovery_type = query_params.get("type")
    
    if token and recovery_type == "recovery":
        st.header("Redefinição de Senha")
        st.write("Por favor, insira sua nova senha abaixo.")
        
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirme a nova senha", type="password")
        
        if st.button("Atualizar Senha"):
            if not new_password or not confirm_password:
                st.error("Preencha ambos os campos de senha.")
            elif new_password != confirm_password:
                st.error("As senhas não conferem. Tente novamente.")
            else:
                response = update_user_password(new_password)
                if response.get("error"):
                    st.error(f"Erro ao atualizar a senha: {response['error']}")
                else:
                    st.success("Senha atualizada com sucesso! Você já pode fazer login com a nova senha.")
        st.stop()


# Fluxo principal do app
def main():
    initialize_session_state()
    load_css()
    
    # Antes de continuar, verifica se há parâmetros de redefinição de senha na URL.
    handle_password_reset()
    
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
        render_main_layout()

if __name__ == "__main__":
    main()