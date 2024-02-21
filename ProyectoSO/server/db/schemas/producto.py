#decimos con la flecha que es lo que va a devolver
def product_schema(product)->dict:
    #retornamos un json de un usuario de la bd de mongo
    return{
        "id":str(product["_id"]),
        "nombre":product["nombre"],
        "descripcion":product["descripcion"],
        "precio":product["precio"],
        "stock":product["stock"],
        "categoria":product["categoria"]
    }

#devuelve un listado de usuarios
def products_schema(products)->list:
    #por cada usuario del listado, llamamos a la funcion que convierte a dict y lo ponemos dentro de una lista
    return [product_schema(product) for product in products]