import streamlit as st
import supabase

# 🔑 Credenciais do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email, password):
    """Faz login no sistema e retorna um dicionário com os dados do usuário."""
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        if response and hasattr(response, "user") and response.user:
            user_obj = response.user
            # Converte para dicionário, incluindo display_name dos metadados
            user_data = {
                "email": user_obj.email,
                "id": user_obj.id,
                "display_name": user_obj.user_metadata.get("display_name", "Usuário")  # Nome padrão se não existir
            }
            st.session_state["user"] = user_data
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            return user_data, "✅ Login realizado com sucesso!"
    except Exception as e:
        return None, f"❌ Erro ao logar: {str(e)}"

def sign_up(email, password, confirm_password, display_name):
    """Cria um novo usuário e adiciona display_name nos metadados."""
    if password != confirm_password:
        return None, "❌ As senhas não coincidem!"

    try:
        response = supabase_client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}}  # 🟢 Correção aqui!
        })
        if response and hasattr(response, "user") and response.user:
            return response.user, "📩 Um e-mail de confirmação foi enviado. Verifique sua caixa de entrada."
        return None, "⚠️ Não foi possível criar a conta. Tente novamente."
    except Exception as e:
        return None, f"❌ Erro ao criar conta: {str(e)}"


def reset_password(email):
    """Envia um email para redefinição de senha."""
    try:
        supabase_client.auth.reset_password_for_email(email)
        return f"📩 Um email de recuperação foi enviado para {email}. Verifique sua caixa de entrada."
    except Exception as e:
        return f"⚠️ Erro ao solicitar recuperação de senha: {str(e)}"

def sign_out():
    """Desconecta o usuário."""
    supabase_client.auth.sign_out()
    st.session_state.pop("user", None)
    st.session_state["refresh"] = True  # 🚀 Marca para atualizar

def get_user():
    """Retorna o usuário autenticado (um dicionário)."""
    return st.session_state.get("user")
