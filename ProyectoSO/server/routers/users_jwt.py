from fastapi import Depends,HTTPException,status,APIRouter
from pydantic import BaseModel
#modulos de Autenticazion
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
#vamos a usar fechas para calcular el token
from datetime import datetime,timedelta
from db.models.user import User
from db.client import db_client
#importamos la operacion de schemas
from db.schemas.user import user_schema,users_schema
from db.schemas.user_full import user_schema_full
from bson import ObjectId

#al pasarle un prefijo, ya no tenemos que referirnos a esa ruta principal, en las demas rutas secundarias
router=APIRouter(prefix="/usersjwt",
                 #en la documentacion el tag nos sirve para separar las apis 
                 tags=["/users"],
                 #con esto si no encuentra algo, por default manda esto
                 responses={404:{"message":"No encontrado"}})


#esta clave secreta se hace en cmd con el comando de
#openssl rand -hex 32
secret_key="ee887841c0d5574a4098afb2c4ea7f6d5961774bcee5752e5237ae8b6133caae"

algoritmo_de_ecriptacion="HS256"
#para trabajar con jwt instalamos: pip install "python-jose[cryptography]"
#tambien instalamanos:  pip install "passlib[bcrypt]"s


#contexto de incriptacion
crypt=CryptContext(schemes=["bcrypt"])
#tiempo de vida del token
acces_token_duracion=30 #minuto

#instancia de sistema de autenticazion
#/login 
oauth2=OAuth2PasswordBearer(tokenUrl="login")

def comprobar_user(email: str):
    try:
        #encuentra el usuario
        user=db_client.users.find_one({"email":email})
        #retorna al usuario
        return User(**user)
    except:
        return {"message":"No se ha encontrado el usuario"}

async def auth_user(token:str=Depends(oauth2)):
    try:
        #trae el token y lo desencripta, como al prinicipio fue un json
        #obtenemos el nombre del usuario, que se guardo en "sub"
        email=jwt.decode(token,secret_key,algorithms=algoritmo_de_ecriptacion).get("sub")
        if email is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Fallo en la desencriptacion",
                            headers={"WWW-Authenticate":"Bearer"})
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Expiro el Token",
                            headers={"WWW-Authenticate":"Bearer"})
    return search_user_db(email)

#esta funcion convierte un User a User_bd
def search_user_db(email:str):
    try:
        user=user_schema_full(db_client.users.find_one({"email":email}))
        return user
    except:
        return None



#response_model=
#nos dice que devolvera esta ruta
@router.get("/users",response_model=list())
async def usersjson():
    return users_schema(db_client.users.find())


@router.post("/loginJWT")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    userfound=search_user_db(form.username)
    if userfound==None:
        raise HTTPException(status_code=404,detail={"message":"Correo Equivocado"})
    
    #verificar si la contraseña que nos pasaron es la contraseña encryptada que tenemos 
    verififcacion=crypt.verify(form.password,userfound["password"])

    if not verififcacion:
        raise HTTPException(status_code=404,detail="La contraseña no es correcta")
    #momento en el que el token se da por expirado
    #                      con esto le sumas un minuto mas a la hora
    acces_token_1_expiration=timedelta(minutes=acces_token_duracion)
    #toma la hora actual y le suma 1 minuto
    expire=datetime.utcnow()+acces_token_1_expiration

    #tenemos el token, pero falta encriptarlo
    acces_token={
        "sub":userfound["email"],
        "exp":expire}
    
    acces_token_encriptado=jwt.encode(acces_token,
                                      secret_key
                                      ,algorithm=algoritmo_de_ecriptacion)
    #el token tiene un tiempo de vida
    return {"acces_token":acces_token_encriptado,"token_type":"Bearer"}

@router.post("/register")
#el Depends() significa que esta operacion va a recibir datos pero no depende de nadie
async def register(user:User):
    #si encontro un usuario, no va a dejar registrarse
    if  type(comprobar_user(user.email)) == User:
         #para enviar codigo de error usamos raise
         raise HTTPException(status.HTTP_404_NOT_FOUND,detail={"message":"Usuario existente"})
    
     #        Nombre de la BD, Nombre de la coleccion, consulta

    #transformamos el usuario a un json

    user_dict=dict(user)
    del user_dict["id"]#eliminamos el campo id, por que mongodb, crea un id automaticamente

    user_dict["password"]= crypt.hash(user_dict["password"])
    #obtenemos el id del registro creado
    _id=db_client.users.insert_one(user_dict).inserted_id
    print(_id)
    #con esto decimos que nos traiga el usuario agregado y le pasamos como parametro el id que obtuvimos
    #creamos una funcion que nos devuelva un json con los valores
    new_user=user_schema(db_client.users.find_one({"_id":_id}))
    return new_user

#Operacion que nos da datos de usuario despues de autenticarse
@router.get("/allow")
#no tendremos un usuario, si el current_user no es capaz de devolver un usuario
async def allow_login(user: User = Depends(auth_user)):#esta ruta depende de lo que haga la funcion current_user()
    if user:
        return True
    return False