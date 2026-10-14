from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
import secrets
import string

logger = get_daily_logger()

def generate_auth_token(length: int = 255) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_user_auth(user, password):
    if user is None or password is None:
        return None
    #logger.info(f"[get_user_auth] User: {user} Password: {password}")

    query_result = mysql_query(f"SELECT Id_Sistema FROM TB_DOMCLOUD_USER WHERE Usuario = '{user}' AND Clave = '{password}'")
    if query_result:
        auth_token = generate_auth_token(255)
        mysql_execute(f"UPDATE TB_DOMCLOUD_USER SET Auth_Token_Value = '{auth_token}', Auth_Token_Time = UNIX_TIMESTAMP() WHERE Usuario = '{user}' AND Clave = '{password}'")
        return {"key":"auth_token", "value":auth_token}
    else:
        return None

def auth_token_valid(auth_token):
    #logger.info(f"[auth_token_valid] Token: {auth_token}")
    query_result = mysql_query(f"SELECT Id_Sistema FROM TB_DOMCLOUD_USER WHERE Auth_Token_Value = '{auth_token}' AND (UNIX_TIMESTAMP() - Auth_Token_Time) < 600")
    if query_result:
        # Cada vez que se usa el token de autorizacion, se actualiza el tiempo de expiración
        mysql_execute(f"UPDATE TB_DOMCLOUD_USER SET Auth_Token_Time = UNIX_TIMESTAMP() WHERE Id_Sistema = '{query_result[0]['Id_Sistema']}'")
        return query_result[0]['Id_Sistema']
    else:
        return None
    
def new_auth_token(system):
    if system is None:
        return None
    auth_token = generate_auth_token(255)
    mysql_execute(f"UPDATE TB_DOMCLOUD_USER SET Auth_Token_Value = '{auth_token}', Auth_Token_Time = UNIX_TIMESTAMP() WHERE Id_Sistema = '{system}'")
    return {"key":"auth_token", "value":auth_token}

def get_client_system_by_amazon_key(amazon_key):
    if amazon_key is None:
        return None
    query_result = mysql_query(f"SELECT Id_Sistema FROM TB_DOMCLOUD_USER WHERE Amazon_Key = '{amazon_key}'")
    if query_result:
        return query_result[0]['Id_Sistema']
    else:
        return None
    