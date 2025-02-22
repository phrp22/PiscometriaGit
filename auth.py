import bcrypt
from database import get_user_password, insert_user

def hash_password(password):
    """ Gera um hash seguro para a senha. """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_password, provided_password):
    """ Verifica se a senha digitada corresponde ao hash armazenado. """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def authenticate_user(username, password):
    """ Autentica um usuário verificando a senha no banco de dados. """
    stored_password = get_user_password(username)
    if stored_password and check_password(stored_password, password):
        return True
    return False

def register_user(username, password):
    """ Registra um novo usuário no sistema. """
    hashed_password = hash_password(password)
    return insert_user(username, hashed_password)
