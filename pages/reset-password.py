import streamlit as st
import supabase

# 🔑 Conectar ao Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# 🎯 Captura o token que o Supabase enviou no email
query_params = st.query_params
access_token = query_params.get("access_token", None)

st.title("🔑 Redefinir Senha")

if access_token:
    new_password = st.text_input("Digite sua nova senha", type="password")
    confirm_password = st.text_input("Confirme sua nova senha", type="password")

    if st.button("Atualizar Senha"):
        if new_password == confirm_password:
            try:
                # Atualiza a senha usando o token do email
                supabase_client.auth.update_user(
                    {"password": new_password},
                    access_token=access_token  # 🔹 Necessário para autenticar a mudança de senha
                )
                st.success("✅ Senha redefinida com sucesso! Agora você pode fazer login.")
            except Exception as e:
                st.error(f"⚠️ Erro ao redefinir senha: {str(e)}")
        else:
            st.error("❌ As senhas não coincidem!")
else:
    st.error("⚠️ Token inválido ou ausente. Verifique seu email e tente novamente.")
