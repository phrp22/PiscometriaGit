import streamlit as st
from auth import get_user, sign_out
from professional import is_professional_enabled, enable_professional_area

def render_sidebar(user):
    """Renderiza a sidebar para usuários logados."""
    with st.sidebar:
        st.title("🔑 Bem-vindo!")
        st.write(f"👤 {user['display_name']} ({user['email']})")

        # Botão de logout
        if st.button("🚪 Sair"):
            sign_out()
            st.success("Você saiu com sucesso!")
            st.session_state["refresh"] = True
            st.rerun()

        st.markdown("---")
        # Verifica se a área profissional está habilitada
        if not is_professional_enabled(user["email"]):
            st.write("🔐 Habilitar área do profissional")
            # Botão para exibir campo de digitação da chave
            if st.button("Habilitar área do profissional"):
                st.session_state["show_prof_input"] = True

            # Se a flag estiver ativa, mostra o campo para digitar a chave
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
