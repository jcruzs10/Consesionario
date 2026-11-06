from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
DB_PASSWORD = "tu_password_aqui"  # Reemplaza con tu contraseña de Azure
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

@app.get("/autos")
def get_autos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM autos;")
            result = cursor.fetchall()
            return result
    finally:
        connection.close()