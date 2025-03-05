import streamlit as st 
import pathlib
from auth import get_user, update_password
from layout import render_main_layout
from dashboard import render_dashboard, render_professional_dashboard
from professional import is_professional_enabled
from profile import get_user_profile, render_onboarding_questionnaire, user_has_profile
from st_supabase_connection import SupabaseConnection

# Configuração da página para um visual legal.
# Definimos título, ícone e layout central.
st.set_page_config(
    page_title="Abaeté",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Initialize connection.
conn = st.connection("supabase", type=SupabaseConnection)

# Captura os parâmetros da URL
query_params = st.query_params
recovery_mode = query_params.get("type", [""])[0] == "recovery"

# Para depuração: Exibir parâmetros da URL capturados
st.write("Query Params Capturados:", query_params)

# **Força um reload se a URL não estiver sendo reconhecida corretamente**
if "rerun" not in st.session_state:
    st.session_state["rerun"] = True
    st.rerun()


# Carrega o CCS para estilizar o visual, aplicando no Streamlit um design mais legal.
def load_css():
    css_path = pathlib.Path("assets/styles.css") # Caminho do código de estilo.
    # Se o CSS realmente existir neste arquivo...
    if css_path.exists():
        with open(css_path, "r") as f: # Abrimos o código para leitura.
            css_content = f.read() # Pegamos o conteúdo e guardamos para consulta.
            st.html(f"<style>{css_content}</style>")  # Com st.html, aplicamos o estilo na tela!


# Função para inicializar a sessão e evitar erro na navegação.
def initialize_session_state():
    # Se a sessão ainda não estiver definida...
    if "user" not in st.session_state:
        st.session_state["user"] = None  # Define o usuário como não autenticado.


# Função principal que tudo controla.
# Definindo qual parte do app se desenrola.
def main():
    initialize_session_state()
    load_css()

    if recovery_mode:
        st.info("🔐 Você está no fluxo de recuperação de senha.")
        
        # Debug: Confirmação de que estamos no modo de recuperação
        st.write("✅ Modo de recuperação ativado!")

        new_password = st.text_input("Digite sua nova senha", type="password")
        confirm_password = st.text_input("Confirme sua nova senha", type="password")

        if st.button("Atualizar Senha"):
            if new_password == confirm_password:
                update_password(new_password)
                st.success("✅ Sua senha foi atualizada. Agora você pode fazer login novamente.")
            else:
                st.error("As senhas não coincidem.")
    else:
        user = get_user()  # Obtém os dados do usuário autenticado.


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