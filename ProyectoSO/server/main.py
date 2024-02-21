from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users_jwt,productos

app=FastAPI()

app.include_router(users_jwt.router)
app.include_router(productos.router)
origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/ProyectoSO2024/public/RegistroSesion.html",
    "https://127.0.0.1:5500",
    "https://127.0.0.1:5500/ProyectoSO2024/public/RegistroSesion.html",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/ProyectoSO2024/public/ProductoLista.html",
    "https://127.0.0.1:5500",
    "https://127.0.0.1:5500/ProyectoSO2024/public/ProductoLista.html"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Puedes ajustar los métodos permitidos según tus necesidades
    allow_headers=["*"],  # Puedes ajustar los encabezados permitidos según tus necesidades
)

@app.get('/')
async def root():
    return "hola"