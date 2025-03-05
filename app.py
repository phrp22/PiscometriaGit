import streamlit as st
import pathlib
from auth import get_user, supabase
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire
import streamlit.components.v1 as components

# Configuração da página para um visual legal.
# Definimos título, ícone e layout central.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Injetando JavaScript para extrair o token do fragmento da URL e redirecionar com query params
js_code = """
<script>
  (function() {
    // Verifica se há fragmento na URL
    const hash = window.location.hash;
    if (hash) {
      // Remove o '#' e cria um objeto URLSearchParams
      const params = new URLSearchParams(hash.substring(1));
      // Verifica se existe o token e se o tipo é 'recovery'
      if (params.has('token') && params.get('type') === 'recovery') {
        const token = params.get('token');
        const type = params.get('type');
        // Cria uma nova URL com os parâmetros de consulta
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set('token', token);
        newUrl.searchParams.set('type', type);
        // Remove o fragmento da URL
        newUrl.hash = '';
        // Redireciona para a nova URL
        window.location.replace(newUrl.href);
      }
    }
  })();
</script>
"""

components.html(js_code, height=0)

# Função para carregar o CSS e melhorar o visual
def load_css():
    css_path = pathlib.Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Inicializa a sessão para evitar erros de navegação
def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None

# Página para redefinição de senha
def reset_password_page():
    query_params = st.query_params
    # Verifica se o token de recuperação está presente na URL e se o tipo é "recovery"
    if "token" in query_params and "type" in query_params and query_params["type"][0] == "recovery":
        token = query_params["token"][0]
        st.write("Token de recuperação detectado. Por favor, defina sua nova senha.")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirmar Nova Senha", type="password")
        
        if st.button("Atualizar Senha"):
            if new_password and new_password == confirm_password:
                # Atualiza o usuário com a nova senha.
                # Se o usuário estiver autenticado, supabase.auth.updateUser() usará a sessão atual.
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

# Função principal do app
def main():
    initialize_session_state()
    load_css()

    query_params = st.query_params
    # Se a URL contiver o token de recuperação e o tipo for "recovery", exibe a página de redefinição de senha
    if "token" in query_params and "type" in query_params and query_params["type"][0] == "recovery":
        reset_password_page()
    else:
        # Se o usuário estiver logado, segue com o fluxo normal
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
            # Tela principal (já configurada para conter o botão que envia o e-mail de recuperação)
            render_main_layout()

if __name__ == "__main__":
    main()
