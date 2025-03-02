import uuid
import streamlit as st
from auth import supabase_client
from profile import get_user_profile

import uuid
from auth import supabase_client
from profile import get_user_profile

def create_patient_invitation(professional_id: str, patient_email: str):
    """
    Cria um convite de vinculação entre um profissional e um paciente.
    - `professional_id`: auth_user_id do profissional (UUID).
    - `patient_email`: email do paciente (vamos buscar o auth_user_id dele).
    """

    # Obter o auth_user_id do paciente via email
    patient_auth_id = _get_auth_user_id_by_email(patient_email)
    if not patient_auth_id:
        return False, "Paciente não encontrado."

    # Verificar se o paciente já tem um perfil
    patient_profile = get_user_profile(patient_auth_id)
    if not patient_profile:
        return False, "Paciente não completou o cadastro."

    # Verificar se já existe um convite pendente
    existing_link = supabase_client.from_("professional_patient_link") \
        .select("id, status") \
        .eq("professional_id", professional_id) \
        .eq("patient_id", patient_auth_id) \
        .execute()

    if existing_link and existing_link.data:
        return False, "Convite já enviado."

    # Criar um novo convite
    data = {
        "id": str(uuid.uuid4()),  # Criar um UUID único
        "professional_id": professional_id,
        "patient_id": patient_auth_id,
        "status": "pending"
    }

    response = supabase_client.from_("professional_patient_link").insert(data).execute()

    if hasattr(response, "error") and response.error:
        return False, f"Erro ao criar convite: {response.error.message}"

    return True, None

def accept_invitation(professional_id: str, patient_id: str):
    """
    Atualiza o status do convite para 'accepted'.
    Usado quando o paciente aceita o vínculo.
    """
    update_response = supabase_client.from_("professional_patient_link") \
        .update({"status": "accepted"}) \
        .eq("professional_id", professional_id) \
        .eq("patient_id", patient_id) \
        .execute()

    if hasattr(update_response, "error") and update_response.error:
        return False, f"Erro ao aceitar convite: {update_response.error.message}"

    return True, None

def reject_invitation(professional_id: str, patient_id: str):
    """
    Atualiza o status do convite para 'rejected'.
    Usado quando o paciente recusa o vínculo.
    """
    update_response = supabase_client.from_("professional_patient_link") \
        .update({"status": "rejected"}) \
        .eq("professional_id", professional_id) \
        .eq("patient_id", patient_id) \
        .execute()

    if hasattr(update_response, "error") and update_response.error:
        return False, f"Erro ao recusar convite: {update_response.error.message}"

    return True, None

def list_invitations_for_patient(patient_id: str):
    """
    Lista todos os convites (pendentes ou não) para um paciente específico.
    Retorna uma lista de dicionários contendo os dados.
    """
    response = supabase_client.from_("professional_patient_link") \
        .select("*") \
        .eq("patient_id", patient_id) \
        .execute()

    if response and hasattr(response, "data"):
        return response.data
    return []

def list_invitations_for_professional(professional_id: str):
    """
    Lista todos os convites (pendentes ou não) para um profissional específico.
    """
    response = supabase_client.from_("professional_patient_link") \
        .select("*") \
        .eq("professional_id", professional_id) \
        .execute()

    if response and hasattr(response, "data"):
        return response.data
    return []

def _get_auth_user_id_by_email(email: str) -> str:
    """
    Função interna para obter o auth_user_id do paciente via email.
    Pode buscar no Supabase Auth ou na tabela user_profile, dependendo da sua arquitetura.
    Exemplo: buscar no Supabase Auth.
    """
    # Exemplo de busca no Supabase Auth (pseudocódigo)
    # Em supabase-py, não há método direto para get_user_by_email, então
    # você pode ter que manter um registro no user_profile ou em outra tabela.
    # Vamos assumir que user_profile salva o email e o auth_user_id.
    response = supabase_client.from_("user_profile") \
        .select("auth_user_id") \
        .eq("email", email) \
        .execute()

    if response and hasattr(response, "data") and len(response.data) > 0:
        return response.data[0]["auth_user_id"]
    return None
