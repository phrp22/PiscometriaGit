import bcrypt

def hash_password(password):
    """ Gera um hash seguro para a senha """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_password, provided_password):
    """ Verifica se a senha digitada corresponde ao hash armazenado """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
