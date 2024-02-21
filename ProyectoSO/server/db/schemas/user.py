#decimos con la flecha que es lo que va a devolver
def user_schema(user)->dict:
    #retornamos un json de un usuario de la bd de mongo
    return{
        "id":str(user["_id"]),
        "email":user["email"]
    }

#devuelve un listado de usuarios
def users_schema(users)->list:
    #por cada usuario del listado, llamamos a la funcion que convierte a dict y lo ponemos dentro de una lista
    return [user_schema(user) for user in users]