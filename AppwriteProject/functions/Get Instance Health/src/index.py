import json
from appwrite.client import Client
from appwrite.services.health import Health

def main(req, res):
    client = Client()
    
    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )
    
    try:
        health = Health(client)
    except:
        obj = {
            "error": "health could not be retrieved",
            "statusCode": 500
        }
        return res.json(obj)

    http_status = health.get()
    db_status = health.get_db()
    storage_status = health.get_storage_local()
    cache_status = health.get_cache()
    log_queue = health.get_queue_logs()
    usage_queue = health.get_queue_usage()
    function_queue = health.get_queue_functions()

    health_obj = {
        "HTTP": http_status,
        "Database": db_status,
        "Storage": storage_status,
        "Cache": cache_status,
        "Log Queue": log_queue,
        "Usage Queue": usage_queue,
        "Function Queue": function_queue,
        "statusCode": 200
    }

    return res.json(health_obj)
