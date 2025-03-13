import streamlit as st
from auth import get_user, sign_out
from patient_link import render_pending_invitations, render_patient_invitations, create_patient_invitation
from utils.gender_utils import adjust_gender_ending, get_professional_title
from utils.professional_utils import  render_professional_enable_section, is_professional_enabled, enable_professional_area, get_professional_data
from utils.user_utils import get_user_info
from utils.goals_utils import render_patient_goals, render_add_goal_section 
from utils.scales_utils import render_add_scale_section, render_patient_scales


# 🖥️ Função para renderizar a sidebar.
def render_sidebar(user):
    """
    Renderiza a barra lateral do usuário autenticado.

    Fluxo:
        1. Obtém os dados do usuário autenticado.
        2. Exibe informações básicas como nome e e-mail.
        3. Adiciona um botão de logout.
        4. Se for um profissional, verifica se a área profissional está habilitada.
        5. Se a área profissional não estiver habilitada, exibe a opção para ativação.

    Args:
        user (dict): Dicionário contendo os dados do usuário autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        professional_utils.py → is_professional_enabled()
        professional_utils.py → render_professional_enable_section()
    """
    
    with st.sidebar:
        
        if not user or "id" not in user:
            st.warning("⚠️ Erro: Usuário não autenticado.")
            return

        # Obtém os dados completos do usuário.
        profile = get_user_info(user["id"], full_profile=True) or {} 
        
        # Ajusta a saudação conforme o gênero do usuário.
        saudacao_base = "Bem-vindo" 
        saudacao = adjust_gender_ending(saudacao_base, profile.get("genero", "M"))

        st.markdown(f"**👤 {user['display_name']}**")
        st.markdown(f"✉️ {user['email']}")

        # Botão de logout
        if st.button("Logout 🚪", key="logout"):
            sign_out()

        st.markdown("---")

        # Se a área do profissional já estiver habilitada...
        if is_professional_enabled(user["id"]):
            st.success("✅ Área do profissional habilitada!")  # Confirma a entrada.
        
        # Caso contrário...
        else:
            render_professional_enable_section(user)  # Renderiza o bloqueio da área profissional.



# 🖥️ Função para renderizar a dashboard do paciente.
def render_dashboard():
    """
    Renderiza a dashboard do paciente, mostrando convites pendentes, metas atribuídas e escalas psicométricas.

    Fluxo:
        1. Obtém os dados do usuário autenticado.
        2. Renderiza a sidebar com informações do usuário.
        3. Exibe convites pendentes para vinculação com profissionais.
        4. Exibe as metas do paciente (utilizando render_patient_goals()).
        5. Exibe as escalas psicométricas atribuídas ao paciente, permitindo que ele responda o questionário (utilizando render_patient_scales()).

    Args:
        None (obtém o usuário autenticado internamente).

    Returns:
        None (apenas renderiza a interface).

    Calls:
        render_sidebar()
        patient_link.py → render_patient_invitations()
        goals_utils.py → render_patient_goals()
        scales_utils.py → render_patient_scales()
    """
    user = get_user()  # Obtém os dados do usuário autenticado.
    if not user or "id" not in user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Obtém informações completas do usuário e ajusta a saudação conforme o gênero.
    profile = get_user_info(user["id"], full_profile=True)
    saudacao = adjust_gender_ending("Bem-vindo", profile.get("genero", "M"))

    # Renderiza a sidebar com informações básicas e botão de logout.
    render_sidebar(user)

    # Exibe a saudação personalizada na tela inicial.
    st.header(f"{saudacao}, {user['display_name']}! 🎉")
    st.markdown("---")

    # Exibe os convites pendentes do paciente.
    render_patient_invitations(user)

    st.markdown("---")

    # Exibe as metas atribuídas ao paciente.
    render_patient_goals(user["id"])

    st.markdown("---")

    # Exibe as escalas psicométricas atribuídas ao paciente,
    # permitindo que ele responda o questionário e salve as respostas.
    render_patient_scales(user["id"])


# 🖥️ Função para renderizar a dashboard exclusiva para profissionais habilitados.
def render_professional_dashboard(user):
    """
    Renderiza a dashboard para profissionais habilitados.

    Fluxo:
        1. Obtém os dados do usuário autenticado.
        2. Renderiza a sidebar com informações do usuário.
        3. Exibe um seletor de ações para o profissional, agora utilizando um selectbox, com as opções:
           - "📩 Convidar Paciente"
           - "📜 Visualizar Convites Pendentes"
           - "🎯 Adicionar Meta para Paciente"
           - "📝 Enviar Escala Psicometica"
        4. Executa a ação escolhida:
           - Se for "Convidar Paciente", permite inserir o e-mail e enviar o convite.
           - Se for "Visualizar Convites Pendentes", exibe os convites pendentes.
           - Se for "Adicionar Meta para Paciente", chama render_add_goal_section().
           - Se for "Enviar Escala Psicometica", chama render_add_scale_section() para atribuir uma escala.
    
    Args:
        user (dict): Dicionário contendo os dados do usuário autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        render_sidebar()
        patient_link.py → create_patient_invitation()
        patient_link.py → render_pending_invitations()
        goals_utils.py → render_add_goal_section()
        scales_utils.py → render_add_scale_section()  (função a ser implementada para escalas)
    """
    if not user or "id" not in user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Renderiza a sidebar.
    render_sidebar(user)

    # Obtém as informações completas do profissional.
    profile = get_user_info(user["id"], full_profile=True)

    # Obtém o título do profissional.
    professional_title = get_professional_title(profile)

    # Ajusta a saudação conforme o gênero do profissional.
    saudacao_base = "Bem-vindo"
    saudacao = adjust_gender_ending(saudacao_base, profile.get("genero", "M"))

    st.subheader(f"{saudacao}, {professional_title}! 🎉")

    # --- Seletor de funcionalidades usando selectbox ---
    st.markdown("##### Painel Profissional")
    opcao_selecionada = st.selectbox(
        "🔽 Selecione uma ação:",
        [
            "📩 Convidar Paciente",
            "📜 Visualizar Convites Pendentes",
            "🎯 Adicionar Meta para Paciente",
            "📝 Enviar Escala Psicometica"
        ],
        key="action_select"
    )

    if opcao_selecionada == "📩 Convidar Paciente":
        st.markdown("##### 📩 Convidar Paciente")
        patient_email = st.text_input("Digite o email do paciente:", key="patient_email_input")
        if st.button("Enviar Convite", key="patientlink", use_container_width=True):
            if patient_email:
                success, msg = create_patient_invitation(user["id"], patient_email)
                if success:
                    st.success("✅ Convite enviado com sucesso!")
                else:
                    st.error(f"Erro: {msg}")
            else:
                st.warning("⚠️ Por favor, insira o email do paciente.")
    elif opcao_selecionada == "📜 Visualizar Convites Pendentes":
        st.markdown("##### 📜 Convites Pendentes")
        render_pending_invitations(user["id"])
    elif opcao_selecionada == "🎯 Adicionar Meta para Paciente":
        render_add_goal_section(user)
    elif opcao_selecionada == "📝 Enviar Escala Psicometica":
        # Chama a função para atribuir uma escala ao paciente.
        # Essa função deve ser implementada no módulo scales_utils.py.
        render_add_scale_section(user)
