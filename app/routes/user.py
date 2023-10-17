from fastapi import APIRouter
from models.user import User
from config.db import connection
from schemas.user import user_entity, user_entity
from bson import objectId
import os
from dotenv import load_dotenv


user = APIRouter()
connection = os.os.getenv("CONNECTION_STRING")

def configure():
    load_dotenv()

@user.get('/')
async def find_all_users():
    configure()
    return user_entity(connection.local.user.find())

@user.post('/')
async def create_user(user:User):
    connection.local.user.insert_one(dict(user))
    return user_entity(connection.local.user.find())

@user.put('/{id}')
async def update_user(id,user:User):
    (connection.local.user.find_one_and_update({"_id": objectId(id)}, {
        "$set":dict(user)
    }))
    return user_entity(connection.local.user.find_one({"_id": objectId(id)}))