import streamlit as st
from auth import get_user, sign_out
from patient_link import render_pending_invitations, render_patient_invitations, create_patient_invitation
from utils.gender_utils import adjust_gender_ending, get_professional_title
from utils.professional_utils import  render_professional_enable_section, is_professional_enabled, enable_professional_area, get_professional_data
from utils.user_utils import get_user_info
from utils.goals_utils import render_patient_goals, render_add_goal_section 


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
    Renderiza a dashboard do paciente, mostrando convites pendentes e metas atribuídas.

    Fluxo:
        1. Obtém os dados do usuário autenticado.
        2. Renderiza a sidebar com informações do usuário.
        3. Exibe convites pendentes para vinculação com profissionais.
        4. Exibe as metas do paciente chamando `render_patient_goals()`.

    Args:
        None (Obtém o usuário autenticado internamente).

    Returns:
        None (apenas renderiza a interface).

    Calls:
        render_sidebar()
        patient_link.py → render_patient_invitations()
        dashboard.py → render_patient_goals()
    """

    user = get_user()  # 🔐 Obtém os dados do usuário autenticado.

    if not user or "id" not in user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # 🔍 Obtém as informações completas do usuário.
    profile = get_user_info(user["id"], full_profile=True)
    
    # 🔄 Ajusta a saudação conforme o gênero do usuário.
    saudacao_base = "Bem-vindo"
    saudacao = adjust_gender_ending(saudacao_base, profile.get("genero", "M"))

    # 📌 Renderiza a sidebar.
    render_sidebar(user)

    # 📢 Exibe uma saudação personalizada na tela inicial.
    st.header(f"{saudacao}, {user['display_name']}! 🎉")
    
    st.markdown("---")

    # 📩 Renderiza os convites pendentes do paciente.
    render_patient_invitations(user)

    # 📋 Renderiza as metas do paciente (chama a nova função)
    render_patient_goals(user["id"])


# 🖥️ Função para renderizar a dashboard exclusiva para profissionais habilitados.
def render_professional_dashboard(user):
    """
    Renderiza a dashboard para profissionais habilitados.

    Fluxo:
        1. Obtém os dados do usuário autenticado.
        2. Renderiza a sidebar com informações do usuário.
        3. Exibe um seletor de ações para o profissional (Convidar Paciente, Ver Convites, Adicionar Meta).
        4. Executa a ação escolhida pelo profissional.

    Args:
        user (dict): Dicionário contendo os dados do usuário autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        render_sidebar()
        patient_link.py → create_patient_invitation()
        patient_link.py → render_pending_invitations()
        goals_utils.py → get_linked_patients()
        dashboard.py → render_add_goal_section()
    """
    
    if not user or "id" not in user:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        return

    # Renderiza a sidebar.
    render_sidebar(user)

    #  Obtém as informações completas do profissional.
    profile = get_user_info(user["id"], full_profile=True)

    # Obtém o título do profissional.
    professional_title = get_professional_title(profile)

    # Ajusta a saudação conforme o gênero do profissional.
    saudacao_base = "Bem-vindo" 
    saudacao = adjust_gender_ending(saudacao_base, profile.get("genero", "M"))

    st.subheader(f"{saudacao}, {professional_title}! 🎉")

    # --- Seletor de funcionalidades ---
    st.markdown("##### 🔽 Selecione uma ação:")
    opcao_selecionada = st.radio(
        "",  
        ["📩 Convidar Paciente", "📜 Visualizar Convites Pendentes", "🎯 Adicionar Meta para Paciente"],
        horizontal=True
    )

    # --- Opção 1: Convidar Paciente ---
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

    # --- Opção 2: Visualizar Convites Pendentes ---
    elif opcao_selecionada == "📜 Visualizar Convites Pendentes":
        st.markdown("##### 📜 Convites Pendentes")
        render_pending_invitations(user["id"]) 

    # --- Opção 3: Adicionar Meta para Paciente ---
    elif opcao_selecionada == "🎯 Adicionar Meta para Paciente":
        render_add_goal_section(user)  # ✅ Chamada para a nova função encapsulada

