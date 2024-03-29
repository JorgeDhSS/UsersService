from fastapi import FastAPI
import certifi
import cryptocode
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
import os
from dotenv import load_dotenv

class User(BaseModel):
    name: str
    mail: str
    password: str

def db_connection():
    load_dotenv()
    PASSWORD = os.getenv('DB_PASSWORD')
    uri = "mongodb+srv://admin:"+PASSWORD+"@atlascluster.jskqzzh.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        casino = client.casino
        users = casino.users
    except Exception as e:
        message = e
        users = {}
    return users
app = FastAPI()

#deployment4
@app.post("/create")
async def create(user: User):
    if user.mail != "" and user.name != "" and user.password != "":
        usersDB = db_connection()
        user_row = {"_id": user.mail, "name":user.name, "mail":user.mail, "password": cryptocode.encrypt(user.password,"qwsadd")}
        try:
            responseQuery = usersDB.insert_one(user_row).inserted_id
            codeResponse  = 1
        except Exception as e:
            if hasattr(e, "_OperationFailure__code"):
                if e._OperationFailure__code == 11000:
                    codeResponse  = 11000
                    responseQuery = "Este correo ya se encuentra registrado"
                else:
                    codeResponse  = 0
                    responseQuery = e
            else:
                    codeResponse  = 0
                    responseQuery = e
    else :
        codeResponse  = 0
        responseQuery = "Los campos requeridos están vacíos"
    return {"code": codeResponse, "resonseQuery": responseQuery}
@app.post("/login")
async def login(user: User):
    if user.mail != "" and user.password != "":
        usersDB = db_connection()
        user_row = {"mail":user.mail}
        try:
            userDB = usersDB.find_one(user_row)
            if cryptocode.decrypt(userDB['password'], "qwsadd") == user.password:
                codeResponse  = 1
                responseQuery = "Acceso correcto"
            else:
                codeResponse  = -1
                responseQuery = "Acceso incorrecto"
        except Exception as e:
            return e
    else :
        codeResponse  = 0
        responseQuery = "Los campos requeridos están vacíos"
    return {"code": codeResponse, "resonseQuery": responseQuery}