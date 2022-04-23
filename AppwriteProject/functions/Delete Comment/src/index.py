import json
from appwrite.client import Client
from appwrite.services.database import Database

def main(req, res):
    client = Client()

    database = Database(client)

    user_id = req.env.get('APPWRITE_FUNCTION_USER_ID', None)
    
    comment_collection_id = req.env.get('COMMENTS_COLLECTION_ID')
    
    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )
    
    payload = json.loads(req.payload)
    comment_id = payload["comment_id"]

    if not comment_id:
        obj = {
            "error": "comment_id should not be empty",
            "statusCode": 400
        }
        return res.json(obj)



    try:
        comment = database.get_document(comment_collection_id, comment_id)
    except:
        obj = {
            "error": "error while getting document from database",
            "statusCode": 500
        }
        return res.json(obj)

    author_id = comment["user_id"]

    # check if user is the author of the comment
    if author_id != user_id:
        obj = {
            "error": "user_id is not same as comment author id",
            "statusCode": 400
        }
        return res.json(obj)



    try:
        result = database.delete_document(comment_collection_id, comment_id)
    except:
        obj = {
            "error": "error while deleting document from database",
            "statusCode": 500
        }
        return res.json(obj)



    answer = {
        "statusCode": 204
    }

    return res.json(answer)
