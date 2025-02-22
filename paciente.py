import streamlit as st
from database import listar_escalas, atualizar_status_escala

def paciente_dashboard():
    st.title("Área do Paciente")

    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    if st.session_state.user_type != "Paciente":
        st.error("Acesso restrito a pacientes.")
        return

    st.subheader("Escalas Recebidas")
    escalas = listar_escalas(st.session_state.username)

    if escalas:
        for escala in escalas:
            st.write(f"📋 {escala['escala']} - Status: {escala['status']}")
            if escala["status"] == "pendente":
                if st.button(f"Responder {escala['escala']}", key=escala["escala"]):
                    atualizar_status_escala(st.session_state.username, escala["escala"])
                    st.success(f"Escala {escala['escala']} concluída!")
                    st.rerun()
    else:
        st.warning("Nenhuma escala pendente.")
