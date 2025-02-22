from database import listar_pacientes, enviar_escala, cadastrar_paciente

def profissional_dashboard():
    st.title("Área do Profissional")

    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    if st.session_state.user_type != "Profissional":
        st.error("Acesso restrito a profissionais.")
        return

    st.subheader("Pacientes Cadastrados")
    pacientes = listar_pacientes(st.session_state.username)

    if pacientes:
        paciente_selecionado = st.selectbox("Selecione um paciente", [p["paciente"] for p in pacientes])

        st.subheader("Enviar Escala Psicométrica")
        escalas_disponiveis = ["BAI (Ansiedade)", "BDI (Depressão)", "ASRS (TDAH)", "WAIS (QI)"]
        escala_selecionada = st.selectbox("Escolha a escala", escalas_disponiveis)

        if st.button("Enviar Escala"):
            response = enviar_escala(st.session_state.username, paciente_selecionado, escala_selecionada)
            if response["success"]:
                st.success(response["message"])
            else:
                st.error(response["message"])
    else:
        st.warning("Nenhum paciente cadastrado ainda.")

    if st.button("Sair"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.rerun()