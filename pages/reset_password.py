import streamlit as st
from supabase import create_client
import os
from urllib.parse import urlparse, parse_qs

# 🔑 Configuração do Supabase (certifique-se de que as credenciais estão no st.secrets)
SUPABASE_URL = st.secrets["supabase_url"]
SUPABASE_KEY = st.secrets["supabase_key"]

# Criando a conexão com o Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🎨 Configuração da página
st.set_page_config(page_title="Redefinir Senha", page_icon="🔑", layout="centered")

# 📩 Obtendo a URL atual para verificar se há um token na URL
query_params = st.query_params
token = query_params.get("token")

# 🎯 Se houver um token, o usuário pode redefinir a senha
if token:
    st.title("🔒 Redefinição de Senha")
    st.write("Por favor, insira sua nova senha abaixo.")

    # 📌 Input para a nova senha
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirme a Nova Senha", type="password")

    # 🔄 Verifica se as senhas coincidem
    if st.button("Alterar Senha"):
        if new_password != confirm_password:
            st.error("As senhas não coincidem! 🚨")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
        else:
            # 🔥 Enviando para o Supabase
            response = supabase.auth.api.update_user(token, {"password": new_password})
            if response.get("error"):
                st.error("Erro ao redefinir a senha. Verifique o token ou tente novamente.")
            else:
                st.success("Senha redefinida com sucesso! ✅")
                st.info("Agora você pode fazer login com sua nova senha.")

# 📧 Se não houver token, exibe o formulário para enviar o e-mail de redefinição
else:
    st.title("🔑 Esqueci minha senha")
    st.write("Informe seu e-mail para receber um link de redefinição de senha.")

    email = st.text_input("E-mail", placeholder="Digite seu e-mail")

    if st.button("Enviar Link de Redefinição"):
        if not email:
            st.warning("Por favor, informe um e-mail válido.")
        else:
            # 🔗 Envia um e-mail com o link de redefinição
            response = supabase.auth.api.reset_password_for_email(email)
            if response.get("error"):
                st.error("Erro ao enviar e-mail. Verifique se o e-mail está correto.")
            else:
                st.success("E-mail enviado com sucesso! 📩")
                st.info("Verifique sua caixa de entrada para redefinir a senha.")
