import streamlit as st
from auth import update_password_with_token  # Função customizada a ser implementada conforme a API do Supabase

def render_reset_password():
    st.markdown("# Redefinir Senha")
    
    # Converte os query parameters para um dicionário e tenta extrair "access_token"
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
            # Chama a função para atualizar a senha utilizando o token
            success, message = update_password_with_token(access_token, new_password)
            if success:
                st.success("Senha redefinida com sucesso!")
                # Limpa os query parameters e reinicia o app para atualizar a interface
                st.query_params.from_dict({})
                st.rerun()
            else:
                st.error(message)