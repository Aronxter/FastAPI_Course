from fastapi import APIRouter

router = APIRouter(prefix= "/products",tags=["products"], responses= {404: {"message": "no encontrado"}})
product_list = ["Producto 1", "producto 2", "Producto 3", "Producto 4", "Producto 5"]
@router.get("/")
async def getProducts():
    return product_list

@router.get("/{id}")
async def getProduct(id: int):
    return product_list[id]