import streamlit as st
import supabase

# 🎯 Captura os parâmetros da URL corretamente
query_params = st.experimental_get_query_params()

# 🛑 Mostra todos os parâmetros da URL para depuração
st.write("🔍 Parâmetros da URL:", query_params)

# Tenta capturar o token
access_token = query_params.get("access_token", [None])[0] or query_params.get("token", [None])[0]

# Verifica se o token foi encontrado
if access_token:
    st.success("✅ Token encontrado!")
else:
    st.error("⚠️ Nenhum token encontrado na URL. Verifique o email ou tente novamente.")
