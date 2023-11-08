import logging, os , pytz, json
from rq import Queue
from cpataudit.auditoria import Auditoria

from flask import request, has_request_context
from datetime import datetime
import redis
from functools import wraps


logger = logging.getLogger(__name__)

TIME_ZONE = os.getenv('TIME_ZONE','Chile/Continental')
TIME_FORMAT = os.getenv('TIME_FORMAT',"%Y-%m-%dT%H:%M:%S+03:00")
santiagoTz = pytz.timezone(TIME_ZONE)

HOST_HEADER_NAME = os.getenv('HOST_HEADER_NAME', 'host')


class CollectorException(Exception):
    pass

def register_record(queue,record):
    auditoria = Auditoria()
    try:
        task = queue.enqueue(auditoria.save_audit_register,
                        record, 
                        job_timeout=os.getenv('JOB_TIME_OUT',1800), 
                        result_ttl=os.environ.get('JOB_TTL_TIME', 5000)) 
        logger.info(task.id)
    except Exception:
        logger.exception('No se ha podido registrar la operación')
        logger.error(record)
    

class AuditContext(object):

    def __init__(self, 
                 queue_name: str, 
                 redis_host : str = 'redis',
                 redis_port : int = 6379 ,
                 redis_db : str ='auditoria' ):
        self.queue_name = queue_name
        conn = redis.Redis(host=os.getenv('REDIS_HOST',redis_host), 
                           port=os.getenv('REDIS_PORT',redis_port), 
                           db=os.getenv('REDIS_DB',redis_db))

            # Cola de tareas (tasks)
        self._queue = Queue(os.getenv('QUEUE_NAME'),connection=conn)


    def queue(self):
        return self._queue
    

    
    ACTION_MAP = {
        "POST": "CREAR",
        "GET": "LEER",
        "PATCH": "MODIFICAR",
        "DELETE": "BORRAR",
        "PUT" : "CREAR",
    }

    def web_audit(self,seccion):
        
        def decorator(func):
            logger.debug(f'func: {func}')
            @wraps(func)
            def wrapper(*args,**kwargs):
                logger.debug(kwargs)
                logger.info('Capturando evento de auditoria')
                queue = self.queue()
                record = {}
                #Obtener IP
                if has_request_context():
                    logger.info('No tiene contexto inicializado')
                    record = {}
                    logger.info(request.headers)
                    ip = request.headers[HOST_HEADER_NAME]
                    logger.debug(request.data)
                    record = {
                        "usuario_id": request.headers.get('rut'),
                        "institucion_id" : request.headers.get('oae_id'),
                        "seccion" : seccion,
                        "accion" : self.ACTION_MAP[request.method],
                        "status" : "ok",
                        "periodo_id" :1,
                        "nombre_periodo" :"",
                        "registro_afectado": 1,
                        "detalle": json.loads(request.data),
                        "direccion_ip": ip,
                        "fecha_creacion": datetime.now(santiagoTz).strftime(TIME_FORMAT)
                    } 
                    logger.debug(record)
                error = False
                try:
                    return func(*args,**kwargs)
                except Exception:
                    logger.exception('La ejeucución de la operación a encontrado un error')
                    raise
                finally:
                    #No se logea nada acá, por que ya se ha registrado en el bloque except
                    if error:
                        record['estatus'] = 'error'
                    #Bajo cualquier evento
                    register_record(queue,record)
            
            return wrapper
        return decorator 