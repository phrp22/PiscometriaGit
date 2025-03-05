import streamlit as st
from auth import update_password_with_token  # Função customizada conforme a API do Supabase

def render_reset_password():
    st.markdown("# Redefinir Senha")
    
    # Extrai o token de acesso utilizando apenas a notação de dicionário
    query_params = st.query_params.to_dict()
    access_token = query_params.get("access_token")
    if not access_token:
        st.error("Token de acesso não encontrado na URL. Verifique se você utilizou o link correto.")
        return

    # Exibe o formulário para a nova senha
    new_password = st.text_input("Nova Senha", type="password", key="new_password")
    confirm_password = st.text_input("Confirmar Nova Senha", type="password", key="confirm_new_password")
    
    if st.button("Redefinir Senha"):
        if not new_password or not confirm_password:
            st.warning("Preencha todos os campos.")
        elif new_password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            success, message = update_password_with_token(access_token, new_password)
            if success:
                st.success("Senha redefinida com sucesso!")
                # Limpa os query parameters e reinicia o app para atualizar a interface
                st.query_params.from_dict({})
                st.rerun()
            else:
                st.error(message)

# Não chame render_reset_password() aqui para evitar execução durante o import.
# Deixe que o app.py decida quando chamar essa função.
