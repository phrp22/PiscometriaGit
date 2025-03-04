import streamlit as st

# 🔒 Esconde a sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

# 🎯 Captura os parâmetros da URL
query_params = st.query_params

# 🛑 Mostra todos os parâmetros da URL para depuração
st.write("🔍 Parâmetros da URL:", query_params)

# Tenta capturar o token
access_token = query_params.get("access_token") or query_params.get("token")

# Verifica se o token foi encontrado
if access_token:
    st.success("✅ Token encontrado!")
else:
    st.error("⚠️ Nenhum token encontrado na URL. Verifique o email ou tente novamente.")
