import streamlit as st
import supabase
import requests

# 🔑 Credenciais do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 📡 Criando o cliente Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email, password):
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        if response and hasattr(response, "user") and response.user:
            user_obj = response.user
            # Converte para dicionário:
            user_data = {
                "email": user_obj.email,
                "id": user_obj.id,
                "display_name": user_obj.user_metadata.get("display_name", "Usuário") if hasattr(user_obj, "user_metadata") else "Usuário"
            }
            st.session_state["user"] = user_data
            st.session_state["refresh"] = True
            return user_data, None
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


def update_password_with_token(token: str, new_password: str):
    """
    Atualiza a senha do usuário utilizando o token de recuperação enviado por email.
    
    Parâmetros:
      token (str): Token de acesso extraído da URL.
      new_password (str): Nova senha que será definida.
    
    Retorna:
      tuple: (True, mensagem de sucesso) se sucesso; (False, mensagem de erro) caso contrário.
    """
    supabase_url = st.secrets["SUPABASE_URL"]
    url = f"{supabase_url}/auth/v1/user"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "password": new_password
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return True, "Senha atualizada com sucesso!"
    else:
        try:
            error_message = response.json().get("error_description", "Erro ao atualizar senha.")
        except Exception:
            error_message = "Erro ao atualizar senha."
        return False, error_message


def reset_password(email):
    """Envia um email para redefinição de senha."""
    try:
        supabase_client.auth.reset_password_for_email(email)
        return f"📩 Um email de recuperação foi enviado para {email}."
    except Exception as e:
        return f"⚠️ Erro ao solicitar recuperação de senha: {str(e)}"


def sign_out():
    """Desconecta o usuário."""
    supabase_client.auth.sign_out()
    st.session_state.pop("user", None)
    st.session_state["refresh"] = True  # Marca para atualizar
    st.rerun()  # Força a reexecução do script para atualizar a interface


def get_user():
    return st.session_state.get("user")




