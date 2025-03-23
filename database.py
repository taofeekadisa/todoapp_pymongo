import os
from pymongo import mongo_client
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_CONNECTION_URI = os.environ.get('MONGO_DB_CONNECTION_URI')


client = mongo_client.MongoClient(MONGO_DB_CONNECTION_URI)

user_collection = client["todoapp"]["users"]
todo_collection = client["todoapp"]["todo"]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)