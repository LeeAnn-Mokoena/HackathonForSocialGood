def user_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "UserName": item["UserName"],
        "name": item["name"],
        "email": item["email"],
        "password": item["password"],
        "contactInformation": item["contactInformation"],
        "biography": item["biography"]
    }

def user_entity(entity) -> list:
    return [user_entity(item) for item in entity]