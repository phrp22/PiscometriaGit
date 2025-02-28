import streamlit as st
import supabase

# 🔑 Credenciais do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email, password):
    """Faz login no sistema e recupera o nome do usuário."""
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})

        if response and hasattr(response, "user") and response.user:
            user_obj = response.user

            # 🔍 Recupera o display_name salvo no Supabase
            display_name = user_obj.user_metadata.get("display_name", "Usuário")

            # 🔐 Salva o usuário na sessão
            st.session_state["user"] = {
                "email": user_obj.email,
                "id": user_obj.id,
                "display_name": display_name  # Agora temos o nome salvo!
            }
            st.session_state["refresh"] = True  # 🚀 Marca para atualizar
            return st.session_state["user"], "✅ Login realizado com sucesso!"
    except Exception as e:
        return None, f"❌ Erro ao logar: {str(e)}"

def sign_up(email, password, confirm_password, display_name):
    """Cria um novo usuário no sistema com display name incluído nos metadados."""
    if password != confirm_password:
        return None, "❌ As senhas não coincidem!"

    try:
        response = supabase_client.auth.sign_up({
            "email": email,
            "password": password,
            "data": {"display_name": display_name}
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
    """Retorna o usuário autenticado."""
    return st.session_state.get("user")
