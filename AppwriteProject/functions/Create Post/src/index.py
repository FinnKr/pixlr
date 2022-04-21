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

    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )
    
    post_collection_id = req.env.get('POSTS_COLLECTION_ID')

    payload = json.loads(req.payload)
    title = payload["title"]
    image64 = payload["image64"]

    if not image64 or not title:
        obj = {
            "error": "title and image64 should not be empty",
            "statusCode": 400
        }
        return res.json(obj)

    try:
        imageRes = urlopen(image64)
    except:
        obj = {
            "error": "error while decoding image",
            "statusCode": 500
        }
        return res.json(obj)

    file_name = str(uuid.uuid4()) + ".png"

    try:
        with open(file_name, "wb") as f:
            f.write(imageRes.file.read())
    except:
        obj = {
            "error": "error while writing image file",
            "statusCode": 500
        }
        return res.json(obj)

    try:
        result = storage.create_file("post_images", "unique()", file_name)
    except:
        obj = {
            "error": "error while creating document",
            "statusCode": 500
        }
        return res.json(obj)


    image_id = result["$id"]

    post = {
        "title": title,
        "image_id": image_id,
        "user_id": user_id
    }

    try:
        result = database.create_document(post_collection_id, "unique()", post)
    except:
        obj = {
            "error": "error while creating document",
            "statusCode": 500
        }
        return res.json(obj)


    result["statusCode"] = 201

    try:
        os.remove(file_name)
    except:
        pass

    return res.json(result)
