from appwrite.client import Client

# You can remove imports of services you don't use
from appwrite.services.account import Account
from appwrite.services.avatars import Avatars
from appwrite.services.database import Database
from appwrite.services.functions import Functions
from appwrite.services.health import Health
from appwrite.services.locale import Locale
from appwrite.services.storage import Storage
from appwrite.services.teams import Teams
from appwrite.services.users import Users

"""
  'req' variable has:
    'headers' - object with request headers
    'payload' - object with request body data
    'env' - object with environment variables
  'res' variable has:
    'send(text, status)' - function to return text response. Status code defaults to 200
    'json(obj, status)' - function to return JSON response. Status code defaults to 200
  If an error is thrown, a response with code 500 will be returned.
"""

def main(req, res):
    client = Client()

    # You can remove services you don't use
    account = Account(client)
    avatars = Avatars(client)
    database = Database(client)
    functions = Functions(client)
    health = Health(client)
    locale = Locale(client)
    storage = Storage(client)
    teams = Teams(client)
    users = Users(client)

    user_id = req.env.get('APPWRITE_FUNCTION_USER_ID', None)

    (
    client
        .set_endpoint(req.env.get('APPWRITE_FUNCTION_ENDPOINT', None))
        .set_project(req.env.get('APPWRITE_FUNCTION_PROJECT_ID', None))
        .set_key(req.env.get('APPWRITE_FUNCTION_API_KEY', None))
    )

    comment_collection_id =  req.env.get('COMMENTS_COLLECTION_ID')
    post_collection_id =  req.env.get('POSTS_COLLECTION_ID')


    content = req.payload.content
    post_id = req.payload.post_id

    if not content or not post_id:
        return res.json({
            "error": "content and post_id should not be empty",
        }, 400)

    post = database.get_document(post_collection_id, post_id)

    if not post:
        return res.json({
            "errors": [
                {
                    "post": "Not found"
                }
            ],
        }, 404)

    comment = {
        "content": content,
        "post_id": post_id,
        "user_id": user_id
    }

    result = database.create_document(comment_collection_id, "unique()", comment)

    if not result:
        return res.json({
            "error": "error while creating document",
        }, 500)

    return res.json(result, 201)
    