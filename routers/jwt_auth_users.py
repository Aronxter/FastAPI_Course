from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
ALGORITHM = "HS256"
crypt = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "fce1550b69102fd11be3db6d379508b6cccc58ea230b201d573bd7d1344d3a3b"

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "aaron":{
    "username": "aaron",
    "full_name": "Aaron Morales",
    "email": "correito@gmail.com",
    "disabled": False,
    "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6" # this is crypt.hash("123456")
    },
    "samuel":{
    "username": "samuel",
    "full_name": "Samuel Morales",
    "email": "pipsa@gmail.com",
    "disabled": False,
    "password": "$2a$12$SduE7dE.i3/ygwd0Kol8bOFvEABaoOOlC8JsCSr6wpwB4zl5STU4S"  # this is crypt.hash("654321")
    }
}
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidos", headers={"WWW-Authenticate": "Bearer"})
    try:
        user =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if user is None:
            raise exception
        return search_user(user)
    except JWTError:
        raise exception

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code= 404, detail= "el usuario no esta en la base de datos")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= 401, detail= "contraseña incorrecta")
    
    acces_token = {"sub": user.username, "exp": datetime.now(timezone.utc) + timedelta(minutes= 3)}
    return {"access_token": jwt.encode(acces_token, algorithm=ALGORITHM, key=SECRET_KEY), "token_type": "bearer"}


@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user