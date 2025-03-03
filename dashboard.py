import streamlit as st
import pathlib
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area
from profile import get_user_profile
from gender_utils import adjust_gender_ending
from patient_link import render_patient_invitations, list_invitations_for_patient, create_patient_invitation, accept_invitation, reject_invitation


def render_sidebar(user):
    """Renderiza a sidebar para todos os usuários logados."""
    with st.sidebar:
        profile = get_user_profile(user["id"])
        saudacao_base = "Bem-vindo"
        saudacao = adjust_gender_ending(saudacao_base, profile["genero"]) if profile else saudacao_base

        st.markdown(f"**👤 {saudacao}, {user['display_name']}**")
        st.markdown(f"✉️ [{user['email']}](mailto:{user['email']})")

        # Botão de logout
        if st.button("Logout 🚪", key="logout"):
            sign_out()
            st.session_state["refresh"] = True
            st.rerun()

        st.markdown("---")

        # Inicializa os estados se ainda não existirem
        if "show_prof_input" not in st.session_state:
            st.session_state["show_prof_input"] = False
        if "prof_key" not in st.session_state:
            st.session_state["prof_key"] = ""

        # Opção para habilitar a área do profissional
        if not is_professional_enabled(user["id"]):
            if st.button("🔐 Habilitar área do profissional", key="professional"):
                st.session_state["show_prof_input"] = not st.session_state["show_prof_input"]
                st.rerun()  # Atualiza a interface

            if st.session_state["show_prof_input"]:
                st.session_state["prof_key"] = st.text_input("Digite 'AUTOMATIZEJA' para confirmar:", key="prof_key_input")

                if st.button("✅ Confirmar", key="confirm_professional"):
                    if st.session_state["prof_key"] == "AUTOMATIZEJA":
                        success, msg = enable_professional_area(user["id"], user["email"], user["display_name"])
                        if success:
                            st.session_state["show_prof_input"] = False
                            st.session_state["refresh"] = True
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("❌ Chave incorreta!")

                # Botão para cancelar e esconder o campo
                if st.button("❌ Cancelar", key="cancel_prof_input"):
                    st.session_state["show_prof_input"] = False
                    st.session_state["prof_key"] = ""
                    st.rerun()
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