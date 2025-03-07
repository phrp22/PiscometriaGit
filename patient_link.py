import uuid
import streamlit as st
from auth import supabase_client
from profile import get_user_profile
from utils.date_utils import format_date
from utils.user_utils import get_patient_info


# 📩 Função para criar um convite de vinculação entre um profissional e um paciente.
def create_patient_invitation(professional_id: str, patient_email: str):
    """Cria um convite para vincular um paciente a um profissional usando e-mail."""
    
    st.write(f"🔍 Buscando {patient_email} no banco de dados do sistema.")

    # Buscar informações do paciente pelo e-mail (ID, nome e email)
    patient_info = get_patient_info(patient_email, by_email=True)
    
    if not patient_info["auth_user_id"]:  # Se o ID não foi encontrado
        st.error(f"🚨 Paciente {patient_email} não encontrado no banco.")
        return False, "Paciente não encontrado."

    patient_auth_id = patient_info["auth_user_id"]

    # Verificar se já existe um convite pendente
    existing_link = supabase_client.from_("professional_patient_link") \
        .select("id, status") \
        .eq("professional_id", professional_id) \
        .eq("patient_id", patient_auth_id) \
        .execute()

    if existing_link and existing_link.data:
        st.warning("📩 Convite já foi enviado.")
        return False, "Convite já enviado."

    # Criar um novo convite
    invitation_id = str(uuid.uuid4())
    data = {
        "id": invitation_id,
        "professional_id": professional_id,
        "patient_id": patient_auth_id,
        "status": "pending"
    }

    response = supabase_client.from_("professional_patient_link").insert(data).execute()

    if hasattr(response, "error") and response.error:
        st.error(f"❌ Erro ao criar convite: {response.error.message}")
        return False, f"Erro ao criar convite: {response.error.message}"

    st.cache_data.clear()

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


def list_pending_invitations(professional_id: str):
    """Retorna todos os convites pendentes de um profissional."""

    st.cache_data.clear() 
    
    response = supabase_client.from_("professional_patient_link") \
        .select("id, patient_id, status, created_at") \
        .eq("professional_id", professional_id) \
        .eq("status", "pending") \
        .execute()

    return response.data if response and hasattr(response, "data") else []


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


def render_patient_invitations(user): 
    """Renderiza os convites recebidos para o paciente aceitar ou recusar."""
    invitations = list_invitations_for_patient(user["id"])
    if not invitations:
        return 

    st.markdown("## 📩 Convites Pendentes")

    for inv in invitations:
        if inv["status"] == "pending":
            professional_profile = get_user_profile(inv["professional_id"])
            if professional_profile:
                profissional_nome = professional_profile.get("display_name", "Profissional")
                genero_profissional = professional_profile.get("genero", "M")

                if genero_profissional == "F":
                    titulo = "Dra."
                elif genero_profissional == "N":
                    titulo = "Drx."
                else:
                    titulo = "Dr."

                st.markdown(f"### {titulo} {profissional_nome} deseja se vincular a você.")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Aceitar", key="accept"):  # Chave para aplicar CSS
                    success, msg = accept_invitation(inv["professional_id"], inv["patient_id"])
                    if success:
                        st.success("Convite aceito com sucesso!")
                        st.rerun()
                    else:
                        st.error(msg)

            with col2:
                if st.button("Recusar", key="reject"):  # Chave para aplicar CSS
                    success, msg = reject_invitation(inv["professional_id"], inv["patient_id"])
                    if success:
                        st.success("Convite recusado.")
                        st.rerun()
                    else:
                        st.error(msg)


def render_pending_invitations(professional_id):
    """Renderiza os convites pendentes do profissional, mostrando nome, e-mail e data formatada."""

    st.subheader("📩 Convites Pendentes")

    pending_invitations = list_pending_invitations(professional_id)

    if not pending_invitations:
        st.info("✅ Nenhum convite pendente no momento.")
        return

    for invitation in pending_invitations:
        # Buscar nome e e-mail do paciente pelo ID
        patient_info = get_patient_info(invitation['patient_id'])
        patient_name = patient_info["display_name"]
        patient_email = patient_info["email"]

        # Formatar a data
        dia, mes, ano = format_date(invitation['created_at'])
        formatted_date = f"{dia}/{mes}/{ano}" if dia else "Data inválida"

        # Exibir as informações formatadas
        st.write(f"👤 **Paciente:** {patient_name}")
        st.write(f"📅 **Data de Envio:** {formatted_date}")
        st.write(f"✉️ **E-mail:** {patient_email}")  # Exibindo o e-mail
        st.markdown("---")