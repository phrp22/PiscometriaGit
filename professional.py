import uuid
import streamlit as st
from auth import supabase_client, sign_out 

def is_professional_enabled(email):
    """Verifica se a área profissional está habilitada para o usuário."""
    response = supabase_client.from_("professional").select("area_habilitada").eq("email", email).execute()

    if response and hasattr(response, "data") and response.data:
        return response.data[0].get("area_habilitada", False)
    return False

def enable_professional_area(email, display_name):
    """Habilita a área do profissional sem duplicação de registros."""
    
    # Verifica se o email já existe
    response = supabase_client.from_("professional").select("email").eq("email", email).execute()

    if response and hasattr(response, "data") and response.data:
        # Se o email já existe, apenas atualiza o campo `area_habilitada`
        update_response = supabase_client.from_("professional").update({"area_habilitada": True}).eq("email", email).execute()
        
        if hasattr(update_response, "error") and update_response.error:
            return False, f"Erro ao atualizar: {update_response.error.message}"
        
        return True, "Área do profissional habilitada com sucesso! ✅✅✅"

    # Se o email não existir, cria um novo registro
    new_uuid = str(uuid.uuid4())
    data = {
        "id": new_uuid,
        "email": email,
        "display_name": display_name,
        "area_habilitada": True
    }
    
    insert_response = supabase_client.from_("professional").insert(data).execute()

    if hasattr(insert_response, "error") and insert_response.error:
        return False, f"Erro ao criar registro: {insert_response.error.message}"
    
    return True, "Área do profissional habilitada com sucesso! ✅✅✅"

def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""

    with st.sidebar:
        st.markdown(f"**👤 Bem-vindo, {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")
        st.success("✅ Área do profissional habilitada!")

        # 🔴 Botão de Logout estilizado
        if st.button("🔓 Logout"):
            sign_out()
            st.session_state.clear()
            st.rerun()

    st.title(f"🎉 Bem-vindo, {user['display_name']}!")
    st.markdown("### 📊 Painel de Controle Profissional")
    
    st.metric(label="📁 Pacientes cadastrados", value="42")
    st.metric(label="📊 Avaliações realizadas", value="128")
    st.metric(label="📆 Última atualização", value="Hoje")

    st.markdown("---")
    st.info("🔍 Novos recursos serão adicionados em breve!")
