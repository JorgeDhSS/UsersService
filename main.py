from fastapi import FastAPI
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel

class User(BaseModel):
    name: str
    mail: str
    password: str

uri = 
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    message = "Pinged your deployment. You successfully connected to MongoDB!"
except Exception as e:
    message = e
app = FastAPI()


@app.post("/create")
async def create(item: User):
    casino = client.casino
    users = casino.users
    user_row = {"_id": item.mail, "name":item.name, "mail":item.mail, "password":item.password}
    #user_row.pop('_id', None)
    try:
        responseQuery = users.insert_one(user_row).inserted_id
    except Exception as e:
        responseQuery = e
    return {responseQuery}
