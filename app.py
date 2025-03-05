import streamlit as st
import pathlib
from auth import supabase_client as supabase
from auth import get_user
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

# Função para carregar o CSS e melhorar o visual.
def load_css():
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Função para mover parâmetros do hash para a query string.
def move_hash_to_query():
    st.components.v1.html(
        """
        <script>
        // Se houver hash na URL e não houver parâmetros na query, move o hash para a query string e recarrega.
        if (window.location.hash && !window.location.search) {
            const hash = window.location.hash.substring(1);
            const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?" + hash;
            window.history.replaceState(null, null, newUrl);
            window.location.reload();
        }
        </script>
        """,
        height=0
    )


# Inicializa a sessão para evitar erros de navegação.
def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None

# Página para redefinição de senha.
def reset_password_page():
    query_params = st.query_params  # Agora usando st.query_params
    # Verifica se o token de recuperação está presente na URL.
    if "access_token" in query_params:
        token = query_params["access_token"][0]
        st.write("Token de recuperação detectado. Por favor, defina sua nova senha.")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirmar Nova Senha", type="password")
        
        if st.button("Atualizar Senha"):
            if new_password and new_password == confirm_password:
                # Atualiza o usuário com a nova senha.
                response = supabase.auth.updateUser({
                    "password": new_password
                })
                if response.get("error"):
                    st.error("Erro ao atualizar senha: " + response["error"]["message"])
                else:
                    st.success("Senha atualizada com sucesso! Você já pode fazer login com sua nova senha.")
            else:
                st.error("As senhas não coincidem ou estão vazias.")
    else:
        st.info("Nenhum token de recuperação encontrado na URL.")

# Função principal do app.
def main():
    initialize_session_state()
    load_css()
    move_hash_to_query()  # Move os parâmetros do hash para a query string.
    
    query_params = st.query_params
    if "access_token" in query_params:
        reset_password_page()
    else:
        # Se o usuário estiver logado, segue com o fluxo normal.
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
            # Tela principal (já configurada para conter o botão que envia o e-mail de recuperação).
            render_main_layout()

if __name__ == "__main__":
    main()
