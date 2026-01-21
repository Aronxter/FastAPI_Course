from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",tags=["UsersDB"], responses= {status.HTTP_404_NOT_FOUND: {"message": "pipsa"}})


user_list =  []
def search_user(field:str, key):

    try:
        usr = db_client.users.find_one({field:key})
        new_usr = User(**user_schema(usr))
        return new_usr
    except:
        return {"error": "no se ha encontrado el usuario"}
    

@router.get("/", response_model= list)
async def get_users():
    return users_schema(db_client.users.find())
#fastapi se encarga de convertir basemodels en json automaticamente

#path search
@router.get("/{id}")
async def get_user(id:str):
    return search_user("_id", ObjectId(id))
    

#query search
@router.get("/userquery/")
async def get_user(id : str):
    return search_user("_id")

    

@router.post("/",response_model = User, status_code= 201) #post operation
async def post_user(user: User):

    if (type(search_user("email", user.email)) == User):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="usuario ya existente")
    else:
        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user)
    
@router.put("/", response_model= User)
async def put_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:

        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al intentar reemplazar")
    return search_user("_id", ObjectId(user.id))



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al eliminar el usuario")
    
        
