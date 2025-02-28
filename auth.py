import streamlit as st
import supabase

# 🔑 As credenciais do Supabase são protegidas em `st.secrets`
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email, password):
    """Faz login no sistema."""
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        
        if response and hasattr(response, "user") and response.user:
            user = response.user
            st.session_state["user"] = {"email": user.email, "id": user.id}
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            return user, "✅ Login realizado com sucesso!"

    except Exception as e:
        return None, f"❌ Erro ao logar: {str(e)}"

def sign_out():
    """Desconecta o usuário."""
    supabase_client.auth.sign_out()
    st.session_state.pop("user", None)
    st.session_state["refresh"] = True  # 🚀 Marca para atualizar

def get_user():
    """Retorna o usuário autenticado"""
    return st.session_state.get("user")
