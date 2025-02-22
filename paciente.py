import streamlit as st
from database import get_escalas_pendentes, responder_escala_psicometrica

def paciente_page():
    st.title("Área do Paciente")

    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    if st.session_state.user_type != "Paciente":
        st.error("Acesso restrito a pacientes.")
        return

    st.subheader("Escalas Psicométricas Pendentes")

    escalas = get_escalas_pendentes(st.session_state.username)

    if not escalas:
        st.write("Nenhuma escala pendente.")
        return

    for escala in escalas:
        st.write(f"Escala enviada por: {escala['profissional']}")
        resposta = st.slider("Sua resposta:", min_value=1, max_value=5)  # Resposta tipo Likert (1 a 5)
        
        if st.button(f"Responder Escala {escala['id']}"):
            response = responder_escala_psicometrica(escala['id'], resposta)
            if response["success"]:
                st.success("Escala respondida com sucesso!")
                st.rerun()
            else:
                st.error(response["message"])
