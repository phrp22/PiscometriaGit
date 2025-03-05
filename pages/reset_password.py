import streamlit as st
from supabase import create_client
import os
from urllib.parse import urlparse, parse_qs

# 🔑 Conexão com o Supabase (credenciais do st.secrets)
SUPABASE_URL = st.secrets["supabase_url"]
SUPABASE_KEY = st.secrets["supabase_key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📩 Captura da URL atual para extrair o token de redefinição
query_params = st.query_params
token = query_params.get("token")
token_type = query_params.get("type")

# 🎯 Se há um token, permite redefinir a senha
if token and token_type == "recovery":
    st.title("🔒 Redefinição de Senha")
    st.write("Insira sua nova senha abaixo.")

    # 📌 Campos de entrada para a nova senha
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirme a Nova Senha", type="password")

    # 🔄 Botão para alterar a senha
    if st.button("Alterar Senha"):
        if new_password != confirm_password:
            st.error("As senhas não coincidem! 🚨")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
        else:
            # 🔥 Atualiza a senha no Supabase
            response = supabase.auth.api.update_user(token, {"password": new_password})

            if response.get("error"):
                st.error("Erro ao redefinir a senha. O token pode estar expirado.")
            else:
                st.success("Senha redefinida com sucesso! ✅")
                st.info("Agora você pode fazer login com sua nova senha.")

# 📧 Se não houver token, exibe a opção de enviar o e-mail
else:
    st.title("🔑 Esqueci minha senha")
    st.write("Informe seu e-mail para receber um link de redefinição de senha.")

    email = st.text_input("E-mail", placeholder="Digite seu e-mail")

    if st.button("Enviar Link de Redefinição"):
        if not email:
            st.warning("Por favor, informe um e-mail válido.")
        else:
            # 🔗 Envia e-mail via Supabase
            redirect_url = "https://abaete.streamlit.app/pages/reset_password"
            response = supabase.auth.api.reset_password_for_email(email, redirect_to=redirect_url)

            if response.get("error"):
                st.error("Erro ao enviar e-mail. Verifique se o e-mail está correto.")
            else:
                st.success("E-mail enviado com sucesso! 📩")
                st.info("Verifique sua caixa de entrada para redefinir a senha.")
