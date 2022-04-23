import json
import os
import uuid
from urllib.request import urlopen
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.services.storage import Storage

def main(req, res):
    client = Client()

    database = Database(client)
    storage = Storage(client)

    user_id = req.env.get('APPWRITE_FUNCTION_USER_ID', None)
    
    bucket_id = req.env.get('APPWRITE_BUCKET_ID', None)
    post_collection_id = req.env.get('POSTS_COLLECTION_ID')
    
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



    try:
        post = database.get_document(post_collection_id, post_id)
    except:
        obj = {
            "error": "error while getting document from database",
            "statusCode": 500
        }
        return res.json(obj)

    author_id = post["user_id"]
    image_id = post["image_id"]

    # check if user is the author of the post
    if author_id != user_id:
        obj = {
            "error": "user_id is not same as post author id",
            "statusCode": 400
        }
        return res.json(obj)



    try:
        result = database.delete_document(post_collection_id, post_id)
    except:
        obj = {
            "error": "error while deleting document from database",
            "statusCode": 500
        }
        return res.json(obj)

    try:
        result = storage.delete_file(bucket_id, image_id)
    except:
        obj = {
            "error": "error while deleting file from bucket",
            "statusCode": 500
        }
        return res.json(obj)

    answer = {
        "statusCode": 204
    }

    return res.json(answer)
