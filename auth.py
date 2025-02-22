from database import get_user_credentials, insert_user
from utils import hash_password, check_password  # ✅ Agora usamos do utils.py

def authenticate_user(username, password):
    """Autentica um usuário verificando suas credenciais no banco de dados."""
    user_data = get_user_credentials(username)
    
    if not user_data:
        return False, None  # Retorna falso se o usuário não existir

    stored_password = user_data["password"]
    user_type = user_data["user_type"]

    if check_password(stored_password, password):
        return True, user_type  # Autenticação bem-sucedida
    
    return False, None  # Senha incorreta

def register_user(username, password, user_type):
    """Registra um novo usuário no sistema."""
    hashed_password = hash_password(password)  # ✅ Agora usa o utils.py
    return insert_user(username, hashed_password, user_type)
