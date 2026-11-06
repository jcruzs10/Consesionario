from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Permite peticiones del frontend desplegado en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = "examenfinal.mysql.database.azure.com"
DB_USER = "henry"
DB_PASSWORD = "admin1234*"
DB_NAME = "consesionario"
DB_PORT = 3306

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

class Auto(BaseModel):
    marca: str
    modelo: str
    anio: int
    precio: float

# GET: Obtener todos los autos
@app.get("/autos")
def get_autos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM autos")
            return cursor.fetchall()
    finally:
        connection.close()

# POST: Crear un nuevo auto
@app.post("/autos")
def crear_auto(auto: Auto):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO autos (marca, modelo, anio, precio) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (auto.marca, auto.modelo, auto.anio, auto.precio))
            connection.commit()
            return {"message": "Auto guardado con éxito"}
    finally:
        connection.close()

# PUT: Actualizar un auto existente
@app.put("/autos/{auto_id}")
def actualizar_auto(auto_id: int, auto: Auto):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE autos SET marca=%s, modelo=%s, anio=%s, precio=%s WHERE id=%s"
            cursor.execute(sql, (auto.marca, auto.modelo, auto.anio, auto.precio, auto_id))
            connection.commit()
            return {"message": "Auto actualizado con éxito"}
    finally:
        connection.close()

# DELETE: Eliminar un auto
@app.delete("/autos/{auto_id}")
def eliminar_auto(auto_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM autos WHERE id=%s"
            cursor.execute(sql, (auto_id,))
            connection.commit()
            return {"message": "Auto eliminado con éxito"}
    finally:
        connection.close()