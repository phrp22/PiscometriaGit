import streamlit as st
from auth import supabase_client

def user_has_profile(auth_user_id):
    """Retorna True se o usuário já tiver um perfil, False caso contrário."""
    response = supabase_client.from_("user_profile").select("id").eq("auth_user_id", auth_user_id).execute()
    return bool(response.data) if response and hasattr(response, "data") else False

def create_user_profile(auth_user_id, genero, data_nascimento):
    """Cria um registro na tabela user_profile."""
    try:
        data = {
            "auth_user_id": auth_user_id,
            "genero": genero,
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
    st.title("Questionário Inicial")
    st.write("Por favor, preencha suas informações para personalizar a experiência.")

    genero = st.selectbox("Qual seu gênero?", ["Masculino", "Feminino", "Neutro", "Prefiro não informar"])
    data_nascimento = st.date_input("Data de Nascimento")

    if st.button("Salvar"):
        success, msg = create_user_profile(user_id, genero, data_nascimento)
        if success:
            st.success("Informações salvas com sucesso!")
            st.session_state["refresh"] = True
            st.experimental_rerun()
        else:
            st.error(f"Ocorreu um erro: {msg}")
