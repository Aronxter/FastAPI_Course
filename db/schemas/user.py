#queremos transformar el json que sacamos de bases de datos en el modelo user que definimos
def user_schema(user) -> dict:
    return{"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]