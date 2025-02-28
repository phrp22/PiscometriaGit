import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, render_professional_dashboard, enable_professional_area

def render_sidebar(user):
    """Renderiza a sidebar para usuários logados."""
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.write(f"👤 {user['display_name']} ({user['email']})")
        
        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()
        
        st.markdown("---")
        # Verifica se a área profissional está habilitada
        if not is_professional_enabled(user["email"]):
            st.write("🔐 Habilitar área do profissional")
            if st.button("Habilitar área do profissional"):
                st.session_state["show_prof_input"] = True
            if st.session_state.get("show_prof_input", False):
                prof_key = st.text_input("Digite a chave do profissional", key="prof_key_input")
                if prof_key:
                    if prof_key == "automatizeja":
                        success, msg = enable_professional_area(user["email"], user["display_name"])
                        if success:
                            st.success(msg)
                            st.session_state["refresh"] = True
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Chave incorreta!")
        else:
            st.info("Área do profissional habilitada!")

def render_dashboard():
    """Renderiza o dashboard para usuários autenticados."""
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    render_sidebar(user)
    st.title(f"🎉 Bem-vindo, {user['display_name']}!")
    st.markdown("### 📈 Estatísticas recentes")
    st.metric(label="Pacientes cadastrados", value="42")
    st.metric(label="Avaliações concluídas", value="120")

import streamlit as st
from auth import get_user, sign_out

def render_professional_sidebar(user):
    """Renderiza a sidebar para a dashboard profissional."""
    with st.sidebar:
        st.title("Área Profissional Habilitada")
        st.write(f"Bem-vindo, {user['display_name']}!")
        st.write(f"Email: {user['email']}")
        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

def render_professional_dashboard():
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta área.")
        return

    render_professional_sidebar(user)
    
    # Conteúdo principal do dashboard profissional:
    st.title("Dashboard Profissional")
    st.markdown("### Funcionalidades exclusivas para profissionais")
    st.markdown("Aqui você pode acessar relatórios, configurar sua área, e muito mais!")
    # Adicione aqui os widgets e funcionalidades específicas para profissionais.
