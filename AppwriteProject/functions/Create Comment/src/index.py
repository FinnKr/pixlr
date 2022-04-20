import json
from appwrite.client import Client
from appwrite.services.database import Database

def main(req, res):
    client = Client()

    database = Database(client)

    user_id = req.env.get('APPWRITE_FUNCTION_USER_ID', None)

    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )

    comment_collection_id =  req.env.get('COMMENTS_COLLECTION_ID')
    post_collection_id =  req.env.get('POSTS_COLLECTION_ID')

    payload = json.loads(req.payload)
    content = payload["content"]
    post_id = payload["post_id"]

    if not content or not post_id:
        obj = {
            "error": "content and post_id should not be empty",
            "statusCode": 400
        }
        return res.json(obj)

    try:
        post = database.get_document(post_collection_id, post_id)
    except:
        obj = {
            "error": "Post not found",
            "statusCode": 404
        }
        return res.json(obj)

    comment = {
        "content": content,
        "post_id": post_id,
        "user_id": user_id
    }

    try:
        result = database.create_document(comment_collection_id, "unique()", comment)
    except:
        obj = {
            "error": "error while creating document",
            "statusCode": 500
        }
        return res.json(obj)

    result["statusCode"] = 201
    return res.json(result)
