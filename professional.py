import streamlit as st
from auth import supabase_client, sign_out
from patient_link import create_patient_invitation  # Importe a função do seu novo módulo


def is_professional_enabled(auth_user_id):
    """Verifica se a área profissional está habilitada para o usuário usando auth_user_id."""
    response = supabase_client.from_("professional").select("area_habilitada").eq("auth_user_id", auth_user_id).execute()

    if response and hasattr(response, "data") and response.data:
        return response.data[0].get("area_habilitada", False)
    return False

def enable_professional_area(auth_user_id, email, display_name):
    """Habilita a área do profissional sem duplicação de registros, agora usando `auth_user_id` corretamente."""

    # Verifica se já existe um registro para esse usuário
    response = supabase_client.from_("professional").select("auth_user_id").eq("auth_user_id", auth_user_id).execute()

    if response and hasattr(response, "data") and response.data:
        # Se já existir, apenas atualiza `area_habilitada`
        update_response = supabase_client.from_("professional").update({"area_habilitada": True}).eq("auth_user_id", auth_user_id).execute()

        if hasattr(update_response, "error") and update_response.error:
            return False, f"Erro ao atualizar: {update_response.error.message}"
        
        return True, None

    # Se não existir, cria um novo registro SEM a coluna `id`
    data = {
        "auth_user_id": auth_user_id,  # Agora usamos o UUID da autenticação
        "email": email,
        "display_name": display_name,
        "area_habilitada": True
    }
    
    # Insere o novo registro
    insert_response = supabase_client.from_("professional").insert(data).execute()

    if hasattr(insert_response, "error") and insert_response.error:
        return False, f"Erro ao criar registro: {insert_response.error.message}"
    
    return True, None


def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    
    # 🔴 Chamar a sidebar antes de exibir qualquer conteúdo
    render_sidebar(user)

    st.title(f"🎉 Bem-vindo, {user['display_name']}!")
    st.markdown("### 📊 Painel de Controle Profissional")

    # Seção de métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Pacientes cadastrados", value="42")
    with col2:
        st.metric(label="Avaliações realizadas", value="128")
    with col3:
        st.metric(label="Última atualização", value="Hoje")

    st.markdown("---")
    st.info("🔍 Novos recursos serão adicionados em breve!")

    # NOVA SEÇÃO: Convidar Pacientes
    st.markdown("## Convidar Paciente")
    st.write("Digite o email do paciente para enviar um convite de vinculação:")
    patient_email = st.text_input("Email do Paciente", key="patient_email_input")
    
    if st.button("Enviar Convite"):
        if patient_email:
            success, msg = create_patient_invitation(user["id"], patient_email)
            if success:
                st.success("Convite enviado com sucesso!")
            else:
                st.error(f"Erro: {msg}")
        else:
            st.warning("Por favor, insira o email do paciente.")

