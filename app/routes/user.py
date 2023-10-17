from fastapi import APIRouter
from models.user import User
from config.db import connection
from schemas.user import userEntity, usersEntity
from bson import objectId

user = APIRouter()

@user.get('/')
async def find_all_users():
    return usersEntity(connection.local.user.find())

@user.post('/')
async def create_user(user:User):
    connection.local.user.insert_one(dict(user))
    return usersEntity(connection.local.user.find())

@user.put('/{id}')
async def update_user(id,user:User):
    (connection.local.user.find_one_and_update({"_id": objectId(id)}, {
        "$set":dict(user)
    }))
    return userEntity(connection.local.user.find_one({"_id": objectId(id)}))