import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, render_professional_dashboard, enable_professional_area
from profile import get_user_profile
from gender_utils import adjust_gender_ending  # Importa a função para ajustar saudações

import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area
from profile import get_user_profile
from gender_utils import adjust_gender_ending

def render_sidebar(user):
    # Inicializa o flag se ainda não estiver definido
    st.session_state["show_prof_input"] = False

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
        if not is_professional_enabled(user["id"]):
            st.write("Área do Profissional")
            # Só altera o flag se o usuário clicar neste botão
            if st.button("🔐 Habilitar área do profissional"):
                st.session_state["show_prof_input"] = True
            # Exibe o campo de texto apenas se o flag estiver True
            if st.session_state.get("show_prof_input", False):
                prof_key = st.text_input("Digite 'AUTOMATIZEJA' para confirmar:", key="prof_key_input")
                if prof_key:
                    if prof_key == "AUTOMATIZEJA":
                        success, msg = enable_professional_area(user["id"], user["email"], user["display_name"])
                        if success:
                            st.session_state["refresh"] = True
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("❌ Chave incorreta!")
        else:
            st.success("✅ Área do profissional habilitada!")

def render_dashboard():
    """Renderiza o dashboard para usuários autenticados."""
    user = get_user()
    if not user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Renderiza a sidebar com informações e opções
    render_sidebar(user)

    # Busca o perfil para personalizar a saudação do dashboard
    profile = get_user_profile(user["id"])
    saudacao_base = "Bem-vindo"
    if profile and profile.get("genero"):
        saudacao = adjust_gender_ending(saudacao_base, profile["genero"])
    else:
        saudacao = saudacao_base

    st.title(f"🎉 {saudacao}, {user['display_name']}!")
    st.markdown("### 📈 Estatísticas recentes")
    
    # Exibe algumas métricas usando colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Pacientes cadastrados", value="42")
    with col2:
        st.metric(label="Avaliações concluídas", value="120")
    with col3:
        st.metric(label="Consultas agendadas", value="15")
    
    st.markdown("---")
    st.subheader("Últimas Atividades")
    st.write("Aqui você pode exibir logs, gráficos ou outras informações relevantes para o usuário.")
    
    # Exemplo de gráfico de linha
    data = {
        "Pacientes": [10, 20, 30, 40, 50],
        "Avaliações": [5, 15, 25, 35, 45]
    }
    st.line_chart(data)

    st.markdown("---")
    st.write("Outros componentes e informações podem ser adicionados aqui conforme a evolução do sistema.")
