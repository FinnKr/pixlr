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
            "text": {
                "error": "content and post_id should not be empty"
            },
            "status_code": 400
        }
        return res.json(obj)

    post = database.get_document(post_collection_id, post_id)

    if not post:
        return res.json({
            "errors": [
                {
                    "post": "Not found"
                }
            ]
        }, 404)

    comment = {
        "content": content,
        "post_id": post_id,
        "user_id": user_id
    }

    result = database.create_document(comment_collection_id, "unique()", comment)

    if not result:
        return res.json({
            "error": "error while creating document"
        }, 500)

    return res.json(result, 201)
