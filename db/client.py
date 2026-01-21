from pymongo import MongoClient
import sys
#Base de datos local
#db_client = MongoClient().local

sys.path.append("C:\\Users\\PC\\Desktop\\FastAPI_Course-main\\Fastapi\\env_var")
from variables import link
#Base de datos remota
db_client = MongoClient(link).test