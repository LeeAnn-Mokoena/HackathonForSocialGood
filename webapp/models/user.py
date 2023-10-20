from pydantic import BaseModel
import uuid

class User(BaseModel):
    userId: str
    userName: str
    name: str
    email: str
    password:str
    contactInformation: str
    biography: str

