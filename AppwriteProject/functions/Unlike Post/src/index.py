import json
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.query import Query

def main(req, res):
    client = Client()

    database = Database(client)

    user_id = req.env.get('APPWRITE_FUNCTION_USER_ID', None)
    
    post_collection_id = req.env.get('POST_COLLECTION_ID')
    like_collection_id = req.env.get('LIKE_COLLECTION_ID')
    
    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )
    
    payload = json.loads(req.payload)

    post_id = payload["post_id"]

    if not post_id:
        obj = {
            "error": "post_id should not be empty",
            "statusCode": 400
        }
        return res.json(obj)



    # Check if post is liked
    try:
        result = database.list_documents(like_collection_id,[Query.equal('user_id', user_id), Query.equal('post_id', post_id)])
    except:
        obj = {
            "error": "error while querying document from database",
            "statusCode": 500
        }
        return res.json(obj)

    if result["total"] == 0:
        obj = {
            "error": "post is not liked",
            "statusCode": 400
        }
        return res.json(obj)

    like_id = result["documents"][0]["$id"]

    """
    # verify that the post exists
    try:
        post = database.get_document(post_collection_id, post_id)
    except:
        obj = {
            "error": "post does not exist",
            "statusCode": 400
        }
        return res.json(obj)
    """

    try:
        result = database.delete_document(like_collection_id, like_id)
    except:
        obj = {
            "error": "error while deleting document",
            "statusCode": 500
        }
        return res.json(obj)

    answer = {
        "statusCode": 204
    }

    return res.json(answer)
