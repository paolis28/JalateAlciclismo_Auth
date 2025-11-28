from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from src.features.db.db_config import engine, get_db
from src.features.auth.presentation.controller_user import router as auth_router

app = FastAPI()

#Para producción:
#Cuando vayas a producción, cambia los orígenes permitidos por el dominio real de tu frontend:
    # allow_origins=[
    #    "https://tudominio.com",
    #    "https://www.tudominio.com",
    # ],

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API corriendo correctamente"}

@app.get("/test")
def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()  # obtiene el valor simple (1)
            return {"db_status": "Conectado", "result": value}
    except Exception as e:
        print("Error de conexión:", e)
        return {"db_status": "Error", "details": str(e)}
    

#Pasar la instancia de router de las rutas a main, inicializar las apis
#Lo que se hafce en controlador