import streamlit as st
from auth import update_password_with_token  # Função customizada a ser implementada conforme a API do Supabase

def render_reset_password():
    st.markdown("# Redefinir Senha")
    
    # Extraindo o token de acesso usando st.query_params.
    # Pode vir com o nome "access_token" e opcionalmente um parâmetro "type" igual a "recovery"
    access_token = st.query_params.get("access_token") or st.query_params.access_token
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
            # A função update_password_with_token deve realizar a requisição ao endpoint de atualização do Supabase,
            # utilizando o token extraído para autorizar a operação.
            success, message = update_password_with_token(access_token, new_password)
            if success:
                st.success("Senha redefinida com sucesso!")
                # Limpa os query parameters para evitar reuso do token
                st.query_params.clear()
                st.rerun()  # Atualiza a página para refletir as alterações
            else:
                st.error(message)

# Chama a função para renderizar o formulário
render_reset_password()
