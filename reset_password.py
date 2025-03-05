import streamlit as st
from auth import update_password_with_token  # Função customizada conforme a API do Supabase

import streamlit.components.v1 as components

# Script para mover o hash para a query string, se necessário.
components.html(
    """
    <script>
    // Se a URL tiver um hash com "access_token" e não estiver nos parâmetros de consulta...
    if (window.location.hash.includes("access_token") && !window.location.search.includes("access_token")) {
      // Extrai o hash (removendo o #)
      const hash = window.location.hash.substring(1);
      // Adiciona o hash à query string
      const newSearch = window.location.search ? window.location.search + "&" + hash : "?" + hash;
      const newUrl = window.location.origin + window.location.pathname + newSearch;
      // Atualiza a URL sem recarregar a página
      window.history.replaceState(null, "", newUrl);
      // Opcional: recarrega a página para que Streamlit capte os novos query parameters
      window.location.reload();
    }
    </script>
    """,
    height=0
)

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
