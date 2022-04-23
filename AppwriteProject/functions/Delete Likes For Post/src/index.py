import json
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.query import Query

def main(req, res):
    
    data = json.loads(req.env.get('APPWRITE_FUNCTION_EVENT_DATA'))

    post_id = data["$id"]
    collection_id = data["$collection"]

    if collection_id != "posts":
        obj = {
            "statusCode": 200
        }
        return res.json(obj)

    client = Client()

    database = Database(client)
    
    like_collection_id = req.env.get('LIKE_COLLECTION_ID')
    
    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )



    # Get all likes for that post
    try:
        likes = database.list_documents(like_collection_id, [Query.equal('post_id', post_id)])
    except:
        obj = {
            "error": "error while querying documents from database",
            "statusCode": 500
        }
        return res.json(obj)

    if likes["total"] == 0:
        obj = {
            "error": "no likes for that document found",
            "statusCode": 400
        }
        return res.json(obj)
        
    for i in range(likes["total"]):
        try:
            like_id = likes["documents"][i]["$id"]
            result = database.delete_document(like_collection_id, like_id)
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
