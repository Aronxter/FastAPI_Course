from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    desabled: bool

class UserDB(User):
    password: str


users_db = {
    "aaron":{
    "username": "aaron",
    "full_name": "Aaron Morales",
    "email": "correito@gmail.com",
    "desabled": False,
    "password": "123456"
    },
    "samuel":{
    "username": "samuel",
    "full_name": "Samuel Morales",
    "email": "pipsa@gmail.com",
    "desabled": False,
    "password": "654321"
    }
}
 #retornamos un objeto con los datos del user de la db
    
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
#citerio de dependencia



async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidos", headers={"WWW-Authenticate": "Bearer"})
   
    if user.desabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code= 404, detail= "el usuario no esta en la base de datos")
    
    user = search_user_db(form.username)
    if  not (form.password == user.password):
        raise HTTPException(status_code=404, detail= "La password no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"} #realmente el access token deberia ser un mensaje encriptado

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user
