#este fichero se va a usar para gestionar la base de datos
from pymongo import MongoClient

#si no se pasa parametros, se conecta automaticamente a la red local
#ahora con el .FastApi_Example siempre apunta a esa base de datos y solo tendriamos que especificar a las colecciones

#conexion local
#db_client=MongoClient().FastApi_Example

#Base de datos remota
#                                                                                               nombre de la base de datos
db_client=MongoClient("").SO

#s
