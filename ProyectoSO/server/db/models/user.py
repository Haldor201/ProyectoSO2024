from pydantic import BaseModel

class User(BaseModel):
    id:str| None #decimos que el id puede que llegue o puede que este vacio
    email:str
    password:str