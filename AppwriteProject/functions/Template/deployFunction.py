from appwrite.client import Client
from appwrite.services.functions import Functions

client = Client()

function_id = input("Enter function id: ")

(client
  .set_endpoint('https://appwrite.berlin-fn.de/v1') # Your API Endpoint
  .set_project('pixlr') # Your project ID
  .set_key('c2039e72b0f5684579853ec9dfd8d12f96b991e908650622802907fa758601cee155d869577a01a8e513d645b2c690712603f4f41d6ed0030f4ccc1243aa6a9a682ee3509c1804e7f78bb40d90b53e528cff6d64828ddd956388e22e87ab26ba61d5e194b28a0ecac789d62813c580508f8bb5f6cb9cd1bf633a12e44def01e4') # Your secret API key
)

functions = Functions(client)

code_path = 'D:\\Coding\\Hackathon\\Pixlr\\AppwriteProject\\functions\\Create Comment\\code.tar.gz'

result = functions.create_deployment(function_id, "src/index.py", open(code_path, 'rb'), False)
