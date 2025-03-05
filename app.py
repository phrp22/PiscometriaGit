import streamlit as st
import pathlib
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
# Importa o cliente Supabase configurado (supondo que exista em um módulo separado)
import supabase_client  # Este módulo deve conter a função update_user_password()

# Configuração da página para um visual legal.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
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
    # Utiliza a função estável para obter os parâmetros da URL (st.experimental_get_query_params foi substituído por st.get_query_params na versão mais recente)
    query_params = st.get_query_params()
    token = query_params.get("token", [None])[0]
    recovery_type = query_params.get("type", [None])[0]
    
    # Verifica se o token está presente e se o tipo é 'recovery'
    if token and recovery_type == "recovery":
        st.header("Redefinição de Senha")
        st.write("Por favor, insira sua nova senha abaixo.")
        
        # Campos para nova senha e confirmação, com inputs do tipo password para segurança
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirme a nova senha", type="password")
        
        # Ao clicar no botão, valida os campos
        if st.button("Atualizar Senha"):
            if not new_password or not confirm_password:
                st.error("Preencha ambos os campos de senha.")
            elif new_password != confirm_password:
                st.error("As senhas não conferem. Tente novamente.")
            else:
                # Chamada à API do Supabase para atualizar a senha do usuário.
                # Observação: De acordo com a documentação, o token é utilizado no link de verificação,
                # e após a autenticação o updateUser atualiza a senha.
                response = supabase_client.update_user_password(new_password)
                if response.get("error"):
                    st.error(f"Erro ao atualizar a senha: {response['error']}")
                else:
                    st.success("Senha atualizada com sucesso! Você já pode fazer login com a nova senha.")
        # Interrompe a execução do fluxo principal enquanto o usuário está no processo de recuperação.
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
