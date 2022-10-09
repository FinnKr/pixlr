from appwrite.client import Client
from appwrite.services.users import Users


def main(req, res):
    client = Client()
    users = Users(client)

    user_id = req.env.get("APPWRITE_FUNCTION_USER_ID", None)

    (
        client.set_endpoint(req.env.get("APPWRITE_FUNCTION_ENDPOINT", None))
        .set_project(req.env.get("APPWRITE_FUNCTION_PROJECT_ID", None))
        .set_key(req.env.get("APPWRITE_FUNCTION_API_KEY", None))
    )

    try:
        user_list = users.list()
    except:
        obj = {
            "error": "error while querying users",
            "statusCode": 500,
        }
        return res.json(obj)

    users_number = int(user_list["total"])

    result = {
        "user_number": users_number,
        "statusCode": 200,
    }

    return res.json(result)
