import streamlit as st
import datetime
from auth import supabase_client

def user_has_profile(auth_user_id):
    """Verifica se o usuário já tem um perfil no Supabase."""
    response = supabase_client.from_("user_profile").select("auth_user_id").eq("auth_user_id", auth_user_id).execute()
    return bool(response.data) if response and hasattr(response, "data") else False

def get_display_name_from_auth():
    """Busca o display_name do usuário autenticado no Supabase Auth."""
    user_response = supabase_client.auth.get_user()

    if not user_response or not user_response.user:
        return "Usuário"

    user_metadata = user_response.user.user_metadata if user_response.user.user_metadata else {}
    return user_metadata.get("display_name", "Usuário")

def create_user_profile(auth_user_id, email, genero, data_nascimento):
    """Cria um perfil do usuário no Supabase."""
    try:
        # Verifica se o usuário está autenticado corretamente
        user_response = supabase_client.auth.get_user()
        if not user_response or not user_response.user:
            return False, "Erro: Usuário não autenticado."

        # Obtém metadata do usuário
        user_metadata = user_response.user.user_metadata if user_response.user.user_metadata else {}
        display_name = user_metadata.get("display_name", "Usuário")

        # Mapeamento de gênero
        genero_map = {"Masculino": "M", "Feminino": "F", "Não-binário": "N"}
        genero_abreviado = genero_map.get(genero, "N")

        # Converte data de nascimento para o formato esperado
        data_nascimento_str = data_nascimento.strftime("%Y-%m-%d") if data_nascimento else None

        # Dados para inserção no banco
        data = {
            "auth_user_id": auth_user_id,
            "email": email,
            "genero": genero_abreviado,
            "data_nascimento": data_nascimento_str,
            "display_name": display_name
        }

        response = supabase_client.from_("user_profile").insert(data).execute()
        if hasattr(response, "error") and response.error:
            return False, response.error.message
        return True, None
    except Exception as e:
        return False, str(e)

def get_user_profile(auth_user_id):
    """Retorna o perfil do usuário (ou None se não existir)."""
    response = supabase_client.from_("user_profile").select("*").eq("auth_user_id", auth_user_id).execute()
    if response and hasattr(response, "data") and len(response.data) > 0:
        return response.data[0]
    return None

def render_onboarding_questionnaire(user_id, user_email):
    """Renderiza o questionário inicial do usuário."""
    st.title("Queremos saber um pouco mais sobre você!")
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    genero = st.selectbox("Qual seu gênero?", ["Masculino", "Feminino", "Não-binário"])

    max_date = datetime.date.today()
    min_date = datetime.date(1900, 1, 1)

    data_nascimento = st.date_input(
        "Quando você nasceu?",
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    # Criando botão estilizado
    st.markdown(
        """
        <style>
            div.stButton > button {
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Salvar", key="profile-save", use_container_width=True):
        # Verifica se o usuário está autenticado antes de salvar
        if not user_id:
            st.error("Erro: usuário não autenticado. Faça login novamente.")
            return

        success, msg = create_user_profile(user_id, user_email, genero, data_nascimento)
        if success:
            st.session_state["refresh"] = True
            st.rerun()
        else:
            st.error(f"Ocorreu um erro: {msg}")