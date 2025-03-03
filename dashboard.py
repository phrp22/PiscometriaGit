import streamlit as st
import streamlit.components.v1 as components
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area
from profile import get_user_profile
from gender_utils import adjust_gender_ending
from patient_link import list_invitations_for_patient, create_patient_invitation, accept_invitation, reject_invitation
from styles import inject_css


def render_sidebar(user):
    with st.sidebar:
        profile = get_user_profile(user["id"])
        saudacao = adjust_gender_ending("Bem-vindo", profile["genero"]) if profile else "Bem-vindo"

        st.markdown(f"**👤 {saudacao}, {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")

        if st.button("Logout 🚪"):
            sign_out()
            st.session_state["refresh"] = True
            st.rerun()

        st.markdown("---")

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
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")  # ⬅️ Certifique-se de que essa linha está indentada corretamente
        return  # ⬅️ Retorna para evitar que o código continue executando

    # Busca o perfil do usuário para personalizar a saudação
    profile = get_user_profile(user["id"])
    saudacao_base = "Bem-vindo"
    saudacao = adjust_gender_ending(saudacao_base, profile["genero"]) if profile else saudacao_base

    render_sidebar(user)

    st.title(f"{saudacao}, {user['display_name']}! 🎉")
    st.markdown("### 📈 Estatísticas Recentes")

    # Adiciona a renderização dos convites pendentes
    render_patient_invitations(user)  # ⬅️ Chama a função aqui

    # Exibe algumas métricas usando colunas
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

    # Exemplo de gráfico de linha
    data = {
        "Pacientes": [10, 20, 30, 40, 50],
        "Avaliações": [5, 15, 25, 35, 45]
    }
    st.line_chart(data)

    st.markdown("---")
    st.write("Outros componentes e informações podem ser adicionados conforme a evolução do sistema.")


def render_professional_dashboard(user):
    """Renderiza o dashboard exclusivo para profissionais habilitados."""
    
   # Busca o perfil do usuário para personalizar a saudação
    profile = get_user_profile(user["id"])
    saudacao_base = "Bem-vindo"
    if profile and profile.get("genero"):
        saudacao = adjust_gender_ending(saudacao_base, profile["genero"])
    else:
        saudacao = saudacao_base

    render_sidebar(user)

    st.title(f"{saudacao}, {user['display_name']}! 🎉")
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


def render_patient_invitations(user):
    """Renderiza os convites recebidos para o paciente aceitar ou recusar."""
    invitations = list_invitations_for_patient(user["id"])
    if not invitations:
        return

    st.markdown("## 📩 Convites Pendentes")
    inject_css()

    for inv in invitations:
        if inv["status"] == "pending":
            professional_profile = get_user_profile(inv["professional_id"])
            profissional_nome = professional_profile.get("display_name", "Profissional") if professional_profile else "Profissional"

            st.markdown(f"### {profissional_nome} deseja se vincular a você.")

            col1, col2 = st.columns(2)

            with col1:
                form_accept = f"accept_form_{inv['id']}"
                with st.form(key=form_accept):
                    st.form_submit_button("✅ Aceitar", use_container_width=True)
                    if st.session_state.get(form_accept, False):
                        success, msg = accept_invitation(inv["professional_id"], inv["patient_id"])
                        if success:
                            st.success("Convite aceito com sucesso!")
                            st.rerun()
                        else:
                            st.error(msg)

            with col2:
                form_reject = f"reject_form_{inv['id']}"
                with st.form(key=form_reject):
                    st.form_submit_button("❌ Recusar", use_container_width=True)
                    if st.session_state.get(form_reject, False):
                        success, msg = reject_invitation(inv["professional_id"], inv["patient_id"])
                        if success:
                            st.success("Convite recusado.")
                            st.rerun()
                        else:
                            st.error(msg)
