# pages/reset_password.py

import streamlit as st
import streamlit.components.v1 as components
from auth import update_password_with_token  # Função customizada que faz PUT no endpoint do Supabase

# 1. Primeiro comando do Streamlit deve ser set_page_config (se ainda não tiver no app.py).
#    Se você já chamou st.set_page_config() no app.py, não chame novamente aqui.
#    st.set_page_config(page_title="Redefinir Senha", page_icon="🔑")

def move_hash_to_query_params():
    """
    Injeta um script JavaScript que move o que estiver no hash (#) para a query string (?).
    Isso é necessário porque o token de acesso do Supabase vem no fragmento (#access_token).
    """
    components.html(
        """
        <script>
        window.addEventListener("load", function() {
          if (window.location.hash.includes("access_token") && !window.location.search.includes("access_token")) {
            const hash = window.location.hash.substring(1); // remove o '#'
            const newSearch = window.location.search ? window.location.search + "&" + hash : "?" + hash;
            const newUrl = window.location.origin + window.location.pathname + newSearch;
            window.history.replaceState(null, "", newUrl);
            window.location.reload();
          }
        });
        </script>
        """,
        height=0
    )

def render_reset_password():
    st.title("Redefinição de Senha")

    # 2. Convertemos st.query_params para dicionário e tentamos pegar o "access_token".
    query_params = st.query_params.to_dict()
    access_token = query_params.get("access_token")

    if not access_token:
        st.warning("Token de acesso não encontrado na URL. Por favor, verifique o link.")
        return

    # 3. Exibimos o formulário para o usuário definir a nova senha.
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Nova Senha", type="password")
    
    if st.button("Redefinir"):
        if not new_password or not confirm_password:
            st.warning("Por favor, preencha todos os campos.")
        elif new_password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            success, message = update_password_with_token(access_token, new_password)
            if success:
                st.success("Senha redefinida com sucesso! Você já pode fazer login novamente.")
                # Opcionalmente, limpar query params e reiniciar a página:
                st.query_params.from_dict({})
                st.rerun()
            else:
                st.error(message)

def main():
    # 1. Mover o hash para query params, se existir.
    move_hash_to_query_params()

    # 2. Renderiza o formulário propriamente dito.
    render_reset_password()

# 4. Executamos a função main() assim que a página for acessada.
main()
