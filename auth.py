import streamlit as st
import supabase

# 🔑 As credenciais do Supabase são protegidas em `st.secrets`
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_up(email, password, confirm_password):
    """Cria um novo usuário."""
    if password != confirm_password:
        return None, "❌ As senhas não coincidem!"

    try:
        response = supabase_client.auth.sign_up({"email": email, "password": password})

        if response and hasattr(response, "user") and response.user:
            return response.user, "📩 Um email de confirmação foi enviado. Verifique sua caixa de entrada."
        
        return None, "⚠️ Não foi possível criar a conta. Tente novamente."

    except Exception as e:
        return None, f"❌ Erro ao criar conta: {str(e)}"

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
