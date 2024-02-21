from fastapi import APIRouter,Depends,HTTPException,status
from db.models.producto import Producto
from db.client import db_client
from db.schemas.producto import product_schema,products_schema
from bson import ObjectId

router=APIRouter(prefix="/productos",
                 #en la documentacion el tag nos sirve para separar las apis 
                 tags=["/productos"],
                 #con esto si no encuentra algo, por default manda esto
                 responses={404:{"message":"No encontrado"}})

def comprobar_producto(nombre):
    try:
        producto=db_client.productos.find_one({"nombre":nombre})
        #retorna al usuario
        return Producto(**producto)
    except:
        return {"message":"No se ha encontrado el producto"}

def buscar_producto(id:str):
    try:
        #encuentra el usuario
        product=product_schema(db_client.productos.find_one({"_id":id}))

        #retorna al usuario
        return Producto(**product)
    except:
        raise HTTPException(status_code=404,detail={"message":"No se ha encontrado el producto"}  )  
    
@router.get('/all')
async def getProducts():
    return products_schema(db_client.productos.find())

@router.get('/{product_id}')
async def getProducts(product_id:str):
    return product_schema(db_client.productos.find_one({"_id":ObjectId(product_id)}))

@router.post('/new')
async def new_product(product:Producto):
    #si encontro un usuario, no va a dejar registrarse
    if  type(comprobar_producto(product.nombre)) == Producto:
         #para enviar codigo de error usamos raise
         raise HTTPException(status.HTTP_404_NOT_FOUND,detail={"message":"Producto Existente"})
    
     #        Nombre de la BD, Nombre de la coleccion, consulta

    #transformamos el usuario a un json

    producto_dict=dict(product)
    del producto_dict["id"]#eliminamos el campo id, por que mongodb, crea un id automaticamente

    #obtenemos el id del registro creado
    _id=db_client.productos.insert_one(producto_dict).inserted_id
    print(_id)
    #con esto decimos que nos traiga el usuario agregado y le pasamos como parametro el id que obtuvimos
    #creamos una funcion que nos devuelva un json con los valores
    new_user=product_schema(db_client.productos.find_one({"_id":_id}))
    return new_user

@router.post('/update')
async def update_product(product:Producto):
    product_dict=dict(product)
    del product_dict["id"]
    try:
         #busca un documento con el id que lo pasamos y lo reemplaza
         db_client.productos.find_one_and_replace({
             "_id": ObjectId(product.id)
         },product_dict)#y lo pasamos lo que queremos que cambie
    except:
        raise HTTPException(status_code=404,detail={"message":"no se pudo actualizar el producto"})
    return buscar_producto(ObjectId(product.id))

#Query
@router.delete('/delete')
async def delete_producto(product_id:str):
    found=db_client.productos.find_one_and_delete({
        "_id": ObjectId(product_id)
    })
    if not found:
        raise HTTPException(status_code=404,detail={"message":"no se ha eliminado al usuario"})
    return {"message":"Producto Eliminado"}