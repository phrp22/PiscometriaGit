import uuid
import streamlit as st
from auth import supabase_client, sign_out 

# Função que checa se o profissional está habilitado, sem hesitar,
# Ela consulta o banco e retorna True ou False, pra você usar.
def is_professional_enabled(auth_user_id):
    """Verifica se a área profissional está habilitada para o usuário usando auth_user_id."""
    response = supabase_client.from_("professional").select("area_habilitada").eq("auth_user_id", auth_user_id).execute()

    if response and hasattr(response, "data") and response.data:
        return response.data[0].get("area_habilitada", False)
    return False


# Função para habilitar a área profissional, com elegância e precisão,
# Sem criar registros duplicados, ela cuida da informação.
def enable_professional_area(auth_user_id, email, display_name):
    """Habilita a área do profissional sem duplicação de registros, usando o UUID do Supabase Auth."""
    
    # Primeiro, verifica se já existe um registro para esse usuário
    response = supabase_client.from_("professional").select("auth_user_id").eq("auth_user_id", auth_user_id).execute()

    if response and hasattr(response, "data") and response.data:
        # Se o usuário já existe, apenas atualiza o campo `area_habilitada`
        update_response = supabase_client.from_("professional").update({"area_habilitada": True}).eq("auth_user_id", auth_user_id).execute()
        
        if hasattr(update_response, "error") and update_response.error:
            return False, f"Erro ao atualizar: {update_response.error.message}"
        
        return True, None

    # Se não existir, cria um novo registro com o UUID do Supabase Auth
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


# Função que renderiza o dashboard dos profissionais com maestria,
# Usando a sidebar e métricas para compor a harmonia.
def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    
    # Abre a sidebar, que é um objeto visual de interação,
    # E nela exibe informações do usuário com muita emoção.
    with st.sidebar:
        st.markdown(f"**👤 Bem-vindo, {user['display_name']}**")  # Saudação com o nome em destaque,
        st.markdown(f"✉️ {user['email']}")                        # E o email mostrado, num toque vibrante.
        st.success("✅ Área do profissional habilitada!")        # Mensagem de sucesso, bem iluminada!

        # Botão de Logout, que é um método para sair,
        # Se o usuário clicar, a sessão limpa e o app vai recomeçar.
        if st.button("Logout 🚪"):
            sign_out()                 # Chama a função para desconectar o usuário,
            st.session_state.clear()   # Limpa a sessão, sem nenhum pormenor.
            st.rerun()                 # Roda novamente o app, com vigor e amor.

    # Fora da sidebar, exibe o título e as métricas com atenção,
    st.title(f"🎉 Bem-vindo, {user['display_name']}!")  # Título que saúda com animação,
    st.markdown("### 📊 Painel de Controle Profissional")  # Subtítulo que revela a visão.
    
    # Mostra as métricas, atributos e valores, com precisão,
    st.metric(label="📁 Pacientes cadastrados", value="42")
    st.metric(label="📊 Avaliações realizadas", value="128")
    st.metric(label="📆 Última atualização", value="Hoje")

    # Linha divisória para separar seções com estilo,
    st.markdown("---")
    # Informação adicional, que anuncia novidades com brilho,
    st.info("🔍 Novos recursos serão adicionados em breve!")
