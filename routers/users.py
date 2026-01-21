from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Users"])
#entidad usuario, tipado para validación de datos
class User(BaseModel):
    id: int
    name: str
    email: str

user_list = [
        User(id=1, name="John Doe", email="aaron.com"),
        User(id=2, name="Jane Smith", email="jane.com"),
        User(id=3, name="Alice Johnson", email="alice.com")
    ]

@router.get("/usersjson")
async def get_users_json():
    return [{"id": 1, "name": "John Doe", "email": "aaron.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane.com"},
              {"id": 3, "name": "Alice Johnson", "email": "alice.com"}]

@router.get("/users")
async def get_users():
    return user_list
#fastapi se encarga de convertir basemodels en json automaticamente

#path search
@router.get("/user/{id}")
async def get_user(id : int):
    found = list(filter(lambda user: user.id == id, user_list))
    if not found:
        raise HTTPException(status_code = 404, detail  = "user not found")
    else:
        return found[0]
    


#query search
@router.get("/userquery/")
async def get_user(id : int):
    found = list(filter(lambda user: user.id == id, user_list))
    if not found:
        raise HTTPException(status_code = 404, detail  = "user not found")
    else:
        return found[0]
    

@router.post("/user/",response_model = User, status_code= 201) #post operation
async def post_user(user: User):
    present_id = [u.id for u in user_list]
    if user.id in present_id:
        raise HTTPException(status_code=400, detail="user already exists")
    user_list.append(user)
    return user
    
@router.put("/user/")
async def put_user(user: User):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            return user
    raise HTTPException(status_code=404, detail="usuario no existente")


        
