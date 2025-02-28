import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, render_professional_dashboard, enable_professional_area
from profile import get_user_profile

def render_sidebar(user):
    """Renderiza a sidebar para usuários logados."""
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.markdown(f"**👤 Bem-vindo, {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")
        
        if st.button("Logout 🚪"):
            sign_out()
            st.session_state["refresh"] = True
            st.rerun()
        
        st.markdown("---")
        # Verifica se a área profissional está habilitada
        if not is_professional_enabled(user["email"]):
            st.write("Área do Profissional")
            if st.button("🔐 Habilitar área do profissional"):
                st.session_state["show_prof_input"] = True
            if st.session_state.get("show_prof_input", False):
                prof_key = st.text_input("Digite a chave do profissional", key="prof_key_input")
                if prof_key:
                    if prof_key == "automatizeja":
                        success, msg = enable_professional_area(user["email"], user["display_name"])
                        if success:
                            st.session_state["refresh"] = True
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Chave incorreta!")
        else:
            st.info("Área do profissional habilitada!")


def render_dashboard():
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Busca o perfil
    profile = get_user_profile(user["id"])
    if profile:
        genero = profile.get("genero", None)
        # Lógica simples de saudação
        if genero == "Feminino":
            saudacao = "Bem-vinda"
        elif genero == "Neutro":
            saudacao = "Bem-vinde"
        else:
            saudacao = "Bem-vindo"
    else:
        # Se não tiver perfil, fallback para "Bem-vindo"
        saudacao = "Bem-vindo"

    st.title(f"{saudacao}, {user['display_name']}!")
    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")
