def user_schema_full(user)->dict:
    #retornamos un json de un usuario de la bd de mongo
    return{
        "email":user["email"],
        "password":user["password"]
    }
