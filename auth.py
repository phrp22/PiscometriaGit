import streamlit as st
import supabase

# 🔑 Credenciais do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email, password):
    """Faz login no sistema."""
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        if response and hasattr(response, "user") and response.user:
            st.session_state["user"] = {"email": response.user.email, "id": response.user.id}
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            return response.user, "✅ Login realizado com sucesso!"
    except Exception as e:
        return None, f"❌ Erro ao logar: {str(e)}"
