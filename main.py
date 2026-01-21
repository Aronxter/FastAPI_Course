from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# ROUTERS
app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
# Routers de autenticación
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.mount("/static",StaticFiles(directory= "static"), name= "static")



@app.get("/")
async def root():
    return "hola FastAPI!"

@app.get("/url")
async def url ():
    return{"message": "Hola Fastapi"}

# Ejecuta el servidor con: uvicorn back.main:app --reload
# Accede a la aplicación en: http://127.0.0.1:8000/
# y para la documentación automática en: http://127.0.0.1:8000/docs o redoc
#ctrl + C para detener el servidor
#hay que instala postman para hacer pruebas de API REST pues el explorador no funciona bien con metodos POST, PUT, DELETE
#o thunderclient que es una extensión de vscode
