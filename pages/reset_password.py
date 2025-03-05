import streamlit as st
from supabase import create_client

# 🔑 Conexão com Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔍 Captura parâmetros da URL
query_params = st.query_params
token = query_params.get("token", None)
token_type = query_params.get("type", None)

# 🎨 Interface principal
st.title("🔑 Redefinir Senha")

# 🎯 Se houver um token válido na URL, exibir o formulário de redefinição
if token and token_type == "recovery":
    st.subheader("Digite uma nova senha")

    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirme a Nova Senha", type="password")

    if st.button("Alterar Senha"):
        if not new_password or not confirm_password:
            st.error("Preencha ambos os campos.")
        elif new_password != confirm_password:
            st.error("As senhas não coincidem! 🚨")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
        else:
            # 🔥 Atualiza a senha no Supabase
            response = supabase.auth.api.update_user(token, {"password": new_password})

            if response and response.get("error"):
                st.error("Erro ao redefinir a senha. O token pode estar expirado ou inválido.")
            else:
                st.success("Senha redefinida com sucesso! ✅")
                st.info("Agora você pode fazer login com sua nova senha.")

# 📧 Se não houver token, exibir o formulário para solicitar um novo link por e-mail
else:
    st.subheader("Esqueci minha senha")
    st.write("Digite seu e-mail para receber um link de redefinição.")

    email = st.text_input("E-mail", placeholder="Digite seu e-mail")

    if st.button("Enviar Link de Redefinição"):
        if not email:
            st.warning("Por favor, informe um e-mail válido.")
        else:
            redirect_url = "https://abaete.streamlit.app/pages/reset_password"
            response = supabase.auth.api.reset_password_for_email(email, redirect_to=redirect_url)

            if response and response.get("error"):
                st.error("Erro ao enviar e-mail. Verifique se o e-mail está correto.")
            else:
                st.success("E-mail enviado com sucesso! 📩")
                st.info("Verifique sua caixa de entrada para redefinir a senha.")
