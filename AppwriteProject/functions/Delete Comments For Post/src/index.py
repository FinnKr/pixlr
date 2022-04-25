import json
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.query import Query


def main(req, res):

    data = json.loads(req.env.get("APPWRITE_FUNCTION_EVENT_DATA"))

    post_id = data["$id"]
    collection_id = data["$collection"]

    if collection_id != "posts":
        obj = {"statusCode": 200}
        return res.json(obj)

    client = Client()

    database = Database(client)

    comment_collection_id = req.env.get("COMMENT_COLLECTION_ID")

    (
        client.set_endpoint(req.env.get("APPWRITE_FUNCTION_ENDPOINT", None))
        .set_project(req.env.get("APPWRITE_FUNCTION_PROJECT_ID", None))
        .set_key(req.env.get("APPWRITE_FUNCTION_API_KEY", None))
    )

    # Get all comments for that post
    try:
        comments = database.list_documents(
            comment_collection_id, [Query.equal("post_id", post_id)]
        )
    except:
        obj = {
            "error": "error while querying documents from database",
            "statusCode": 500,
        }
        return res.json(obj)

    comments_total = comments["total"]
    if comments_total == 0:
        obj = {"error": "no comments for that document found", "statusCode": 400}
        return res.json(obj)

    query_size = 25  # number of documents to delete on one go
    status = 0  # status for tracking deletion of documents

    # calculate how many iterations we need for deleting all documents
    iterations = (comments_total // query_size) + 1

    # get documents of database in chunks of query_size
    for i in range(iterations):
        try:
            comment_query = database.list_documents(
                comment_collection_id,
                [Query.equal("post_id", post_id)],
                limit=query_size
            )
        except:
            obj = {
                "error": "error while querying documents from database",
                "statusCode": 500,
            }
            return res.json(obj)

        # on last iterations, less documents need to be deleted
        if i == iterations - 1:
            query_size = comments_total % query_size

        # delete these {query_size} documents:
        for k in range(query_size):
            try:
                comment_id = comment_query["documents"][k]["$id"]
                database.delete_document(comment_collection_id, comment_id)
            except:
                status += 1

    if status > 0:
        obj = {
            "error": f"error while deleting {status} documents from database",
            "statusCode": 500,
        }
        return res.json(obj)

    answer = {"statusCode": 204}

    return res.json(answer)
