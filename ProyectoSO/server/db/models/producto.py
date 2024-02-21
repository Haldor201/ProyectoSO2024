from pydantic import BaseModel

class Producto(BaseModel):
    id:str| None #decimos que el id puede que llegue o puede que este vacio
    nombre:str
    descripcion:str
    precio:float
    stock:int
    categoria:str