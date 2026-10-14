from datetime import datetime
from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from app.client_utils import enqueue_action

logger = get_daily_logger()

def alexa_discover(system):
    logger.info(f"alexa_discover: system={system}")
    return mysql_query(f"SELECT Id, Objeto, Tipo, Grupo_Visual, Icono_Apagado FROM TB_DOMCLOUD_ASSIGN WHERE System_Key = '{system}' AND Id > 0;")
    
def alexa_turn_on(system, objeto):
    logger.info(f"alexa_turn_on: system={system}, objeto={objeto}")
    enqueue_action(system, objeto, action="ON")
    # {"resp_code": "0", "resp_msg": "Ok", "Objeto": "Luz Taller", "Estado": "1", "Ultimo_Update": "2026-08-07 18:13:37" }
    fecha_hora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return {"resp_code": "0", "resp_msg": "Ok", "Objeto": objeto, "Estado": "1", "Ultimo_Update": fecha_hora}

def alexa_turn_off(system, objeto):
    logger.info(f"alexa_turn_off: system={system}, objeto={objeto}")
    enqueue_action(system, objeto, action="OFF")
    fecha_hora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return {"resp_code": "0", "resp_msg": "Ok", "Objeto": objeto, "Estado": "0", "Ultimo_Update": fecha_hora}

def alexa_lock(system, objeto):
    logger.info(f"alexa_lock: system={system}, objeto={objeto}")
    fecha_hora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return {"resp_code": "0", "resp_msg": "Ok", "Objeto": objeto, "Estado": "1", "Ultimo_Update": fecha_hora}

def alexa_unlock(system, objeto):
    logger.info(f"alexa_unlock: system={system}, objeto={objeto}")
    enqueue_action(system, objeto, action="PULSE")
    fecha_hora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return {"resp_code": "0", "resp_msg": "Ok", "Objeto": objeto, "Estado": "0", "Ultimo_Update": fecha_hora}

def alexa_report_state(system, objeto):
    logger.info(f"alexa_report_state: system={system}, objeto={objeto}")
    return mysql_query(
        f"SELECT Id, Objeto, Estado, Grupo_Visual, "
        f"FROM_UNIXTIME(Time_Stamp, '%Y-%m-%d %H:%i:%s') AS Ultimo_Update "
        f"FROM TB_DOMCLOUD_ASSIGN WHERE System_Key = '{system}' AND UPPER(Objeto) = UPPER('{objeto}') AND Id > 0;"
    )