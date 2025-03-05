import streamlit as st
import supabase

def reset_password_page():
    st.set_page_config(
        page_title="Redefinir Senha",
        page_icon="🔑",
        layout="centered"
    )

    # 🔑 Conectar ao Supabase
    try:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
    except KeyError:
        st.error("🚨 Erro: Configurações do Supabase não foram encontradas.")
        st.stop()

    # 🎯 Captura os parâmetros da URL corretamente
    query_params = st.query_params
    access_token = query_params.get("access_token") or query_params.get("token")

    st.title("🔑 Redefinir Senha")

    if not access_token:
        st.error("⚠️ Nenhum token encontrado na URL. Verifique o email ou tente novamente.")
        return

    new_password = st.text_input("Digite sua nova senha", type="password")
    confirm_password = st.text_input("Confirme sua nova senha", type="password")

    if st.button("Atualizar Senha"):
        if new_password != confirm_password:
            st.error("❌ As senhas não coincidem!")
            return

        try:
            response = supabase_client.auth.update_user(
                {"password": new_password},
                access_token=access_token
            )
            if response:
                st.success("✅ Senha redefinida com sucesso! Agora você pode fazer login.")
                st.markdown("[🔑 Ir para Login](https://abaete.streamlit.app/)")
            else:
                st.error("⚠️ Erro ao redefinir a senha. Tente novamente.")
        except Exception as e:
            st.error(f"⚠️ Erro ao redefinir senha: {str(e)}")