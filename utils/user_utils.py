import streamlit as st
from auth import supabase_client


@st.cache_data
def get_patient_info(identifier, by_email=False):
    """
    Busca informações do paciente pelo ID ou pelo e-mail.

    Args:
        identifier (str): auth_user_id ou e-mail do paciente.
        by_email (bool): Se True, faz a busca pelo e-mail. Se False, usa auth_user_id.

    Returns:
        dict: {"auth_user_id": ID, "display_name": Nome, "email": E-mail}
    """
    query = supabase_client.from_("user_profile")

    if by_email:
        response = query.select("auth_user_id, display_name, email").eq("email", identifier).execute()
    else:
        response = query.select("display_name, email").eq("auth_user_id", identifier).execute()

    if response and hasattr(response, "data") and response.data:
        data = response.data[0]
        return {
            "auth_user_id": data.get("auth_user_id", None),
            "display_name": data.get("display_name", "Paciente Desconhecido"),
            "email": data.get("email", "Email não disponível")
        }

    return {"auth_user_id": None, "display_name": "Paciente Desconhecido", "email": "Email não disponível"}
