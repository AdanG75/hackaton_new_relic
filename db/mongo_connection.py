from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from core.settings import setting

uri = setting.get_mongo_uri()
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
act_db = client.hackaton_new_relic


# Send a ping to confirm a successful connection
def ping_mongo():
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
        raise e
