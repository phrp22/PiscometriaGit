import uuid
import streamlit as st
from auth import supabase_client, sign_out  # Certifique-se de que supabase_client está exportado no auth.py

def is_professional_enabled(email):
    """
    Consulta a tabela 'professional' no Supabase para verificar se o usuário
    com o email informado tem a área profissional habilitada.
    """
    response = supabase_client.from_("professional").select("area_habilitada").eq("email", email).execute()

    if response.data:
        data = response.data
        if len(data) > 0:
            return data[0].get("area_habilitada", False)
    return False

def enable_professional_area(email, display_name):
    """
    Verifica se o usuário já está na tabela 'professional'.
    Se já existir, apenas atualiza `area_habilitada` para True.
    Se não existir, insere um novo registro.
    """
    # Verifica se o email já está cadastrado
    response = supabase_client.from_("professional").select("email").eq("email", email).execute()

    if response.data and len(response.data) > 0:
        # Se o email já existe, apenas atualiza o campo `area_habilitada`
        update_response = supabase_client.from_("professional").update({"area_habilitada": True}).eq("email", email).execute()
        
        if update_response.error:
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

    if insert_response.error:
        return False, f"Erro ao criar registro: {insert_response.error.message}"
    
    return True, "Área do profissional habilitada com sucesso! ✅✅✅"


def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""

    # 🔹 Configuração da Sidebar (Menu Lateral)
    with st.sidebar:
        st.markdown("## 👨‍⚕️ Área Profissional")
        st.markdown(f"**👤 Bem-vindo, {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")
        
        # ✅ Mensagem de sucesso dentro de um box verde
        st.success("✅ Área do profissional habilitada com sucesso! ✅✅✅")

        # 🔴 Botão de Logout
        if st.button("🔓 Logout"):
            sign_out()
            st.session_state.clear()
            st.experimental_rerun()
    
    # 🔹 Conteúdo Principal da Dashboard
    st.title(f"🎉 Bem-vindo, {user['display_name']}!")
    st.markdown("### 📊 Painel de Controle Profissional")
    
    # 📈 Estatísticas (pode ser expandido no futuro)
    st.markdown("Aqui você pode acessar funcionalidades exclusivas para profissionais da saúde mental.")
    
    st.metric(label="📁 Pacientes cadastrados", value="42")
    st.metric(label="📊 Avaliações realizadas", value="128")
    st.metric(label="📆 Última atualização", value="Hoje")

    st.markdown("---")
    st.info("🔍 Novos recursos serão adicionados em breve!")