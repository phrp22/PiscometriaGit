import streamlit as st
import supabase

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
error_code = query_params.get("error_code")
error_description = query_params.get("error_description")

st.title("🔑 Redefinir Senha")

if access_token:
    new_password = st.text_input("Digite sua nova senha", type="password")
    confirm_password = st.text_input("Confirme sua nova senha", type="password")

    if st.button("Atualizar Senha"):
        if new_password == confirm_password:
            try:
                # Atualiza a senha no Supabase
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
    st.error("⚠️ O link expirou ou já foi utilizado, tente novamente.")