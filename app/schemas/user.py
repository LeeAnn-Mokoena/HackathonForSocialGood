def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]