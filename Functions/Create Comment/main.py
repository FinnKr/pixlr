# Perform all your imports
from appwrite.client import Client
from appwrite.services.storage import Storage

# Initialise the Appwrite client
client = Client()
client.set_endpoint('https://[HOSTNAME_OR_IP]/v1') # Your API Endpoint
client.set_project('5df5acd0d48c2') # Your project ID
client.set_key('919c2d18fb5d4...a2ae413da83346ad2') # Your secret API key

# Initialise the sttorage SDK with the client object
storage = Storage(client)

# Perform your task
result = storage.list_files()

import json
import requests
import random

def main(request, response):
    payload = json.loads(request.payload or '{}')
    env = request.env

    randomNumber = random.randint(1, 100)
    todo = requests.get(f"https://jsonplaceholder.typicode.com/todos/{randomNumber}").json()

    task = {
        "message": "Hello from Appwrite Functions 👋",
        **todo
    }

    task["trigger"] = {
        "http": "HTTP",
        "schedule": "CRON",
        "event": "Event",
        "unknown": "Unknown"
    }[env['APPWRITE_FUNCTION_TRIGGER']]

    return response.json(task)