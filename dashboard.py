import streamlit as st
import pathlib
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area
from profile import get_user_profile
from gender_utils import adjust_gender_ending
from patient_link import list_invitations_for_patient, create_patient_invitation, accept_invitation, reject_invitation

# 🔹 Função para carregar CSS do arquivo externo
def load_css():
    css_path = pathlib.Path("assets/styles.css")  # Caminho do CSS
    if css_path.exists():  # Verifica se o arquivo existe
        with open(css_path, "r") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Aplica o CSS uma única vez
load_css()

def render_sidebar(user):
    """Renderiza a sidebar para todos os usuários logados."""
    with st.sidebar:
        profile = get_user_profile(user["id"])
        saudacao_base = "Bem-vindo"
        saudacao = adjust_gender_ending(saudacao_base, profile["genero"]) if profile else saudacao_base

        st.markdown(f"**👤 {saudacao}, {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")

        if st.button("Logout 🚪"):
            sign_out()
            st.session_state["refresh"] = True
            st.rerun()

        st.markdown("---")

        # Opção para habilitar a área do profissional
        if not is_professional_enabled(user["id"]):
            if st.button("🔐 Habilitar área do profissional"):
                st.session_state["show_prof_input"] = True
            if st.session_state.get("show_prof_input", False):
                prof_key = st.text_input("Digite 'AUTOMATIZEJA' para confirmar:", key="prof_key_input")
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

    profile = get_user_profile(user["id"])
    saudacao_base = "Bem-vindo"
    saudacao = adjust_gender_ending(saudacao_base, profile["genero"]) if profile else saudacao_base

    render_sidebar(user)

    st.title(f"{saudacao}, {user['display_name']}! 🎉")
    st.markdown("### 📈 Estatísticas Recentes")

    render_patient_invitations(user)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Pacientes cadastrados", value="42")
    with col2:
        st.metric(label="Avaliações concluídas", value="120")
    with col3:
        st.metric(label="Consultas agendadas", value="15")

    st.markdown("---")
    st.subheader("📌 Últimas Atividades")
    st.write("Aqui você pode exibir logs, gráficos ou outras informações relevantes.")

    data = {
        "Pacientes": [10, 20, 30, 40, 50],
        "Avaliações": [5, 15, 25, 35, 45]
    }
    st.line_chart(data)

    st.markdown("---")
    st.write("Outros componentes e informações podem ser adicionados conforme a evolução do sistema.")

def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    
    profile = get_user_profile(user["id"])
    saudacao_base = "Bem-vindo"
    saudacao = adjust_gender_ending(saudacao_base, profile["genero"]) if profile else saudacao_base

    render_sidebar(user)

    st.title(f"{saudacao}, {user['display_name']}! 🎉")
    st.markdown("### 📊 Painel de Controle Profissional")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Pacientes cadastrados", value="42")
    with col2:
        st.metric(label="Avaliações realizadas", value="128")
    with col3:
        st.metric(label="Última atualização", value="Hoje")

    st.markdown("---")
    st.info("🔍 Novos recursos serão adicionados em breve!")

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
                if st.button("✅ Aceitar", key="accept"):  # Chave para aplicar CSS
                    success, msg = accept_invitation(inv["professional_id"], inv["patient_id"])
                    if success:
                        st.success("Convite aceito com sucesso!")
                        st.rerun()
                    else:
                        st.error(msg)

            with col2:
                if st.button("❌ Recusar", key="reject"):  # Chave para aplicar CSS
                    success, msg = reject_invitation(inv["professional_id"], inv["patient_id"])
                    if success:
                        st.success("Convite recusado.")
                        st.rerun()
                    else:
                        st.error(msg)

