import streamlit as st
import datetime
from auth import supabase_client

def user_has_profile(auth_user_id):
    """Retorna True se o usuário já tiver um perfil, False caso contrário."""
    response = supabase_client.from_("user_profile").select("id").eq("auth_user_id", auth_user_id).execute()
    return bool(response.data) if response and hasattr(response, "data") else False

def create_user_profile(auth_user_id, genero, data_nascimento):
    """Cria um registro na tabela user_profile."""
    try:
        # Mapeia a escolha do usuário para M, F ou N
        genero_map = {
            "Masculino": "M",
            "Feminino": "F",
            "Não-binário": "N"
        }
        genero_abreviado = genero_map.get(genero, "M")  # Padrão "M" se não achar

        data = {
            "auth_user_id": auth_user_id,
            "genero": genero_abreviado,  # Salva M, F ou N
            "data_nascimento": data_nascimento.strftime("%Y-%m-%d") if data_nascimento else None
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

def render_onboarding_questionnaire(user_id):
    """Renderiza o questionário inicial para coletar gênero, data de nascimento, etc."""
    st.title("Queremos saber um pouco mais sobre você!")
    st.markdown("<hr style='border:1px solid gray; margin: 30px 0;'>", unsafe_allow_html=True)

    genero = st.selectbox("Qual seu gênero?", ["Masculino", "Feminino", "Não-binário"])

    # Define limites para a data de nascimento
    max_date = datetime.date.today()  # O usuário não pode escolher datas futuras
    min_date = datetime.date(1900, 1, 1)  # Permite qualquer data de nascimento razoável

    data_nascimento = st.date_input(
        "Quando você nasceu?",
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    if st.button("Salvar"):
        success, msg = create_user_profile(user_id, genero, data_nascimento)
        if success:
            st.session_state["refresh"] = True
            st.rerun()
        else:
            st.error(f"Ocorreu um erro: {msg}")
