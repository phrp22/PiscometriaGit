import streamlit as st
import supabase
import uuid

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
        return None, f"Erro ao logar: {str(e)} ❌"

def sign_up(email, password, confirm_password, display_name):
    """Cria um novo usuário no sistema e insere dados extras na tabela de perfis."""
    if password != confirm_password:
        return None, "As senhas não coincidem! ❌"

    try:
        # Cria o usuário via Supabase Auth
        response = supabase_client.auth.sign_up({"email": email, "password": password})
        if response and hasattr(response, "user") and response.user:
            user_obj = response.user

            # Gera um UUID para o perfil do usuário
            new_uuid = str(uuid.uuid4())
            data = {
                "id": new_uuid,
                "email": email,
                "display_name": display_name
            }
            # Insere os dados na tabela user_profiles
            insert_response = supabase_client.from_("user_profiles").insert(data).execute()
            if insert_response.error:
                return None, f"Erro ao criar perfil: {insert_response.error.message}"
            return user_obj, "📩 Um e-mail de confirmação foi enviado. Verifique sua caixa de entrada."
        return None, "⚠️ Não foi possível criar a conta. Tente novamente."
    except Exception as e:
        return None, f"Erro ao criar conta: {str(e)} ❌ "

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
