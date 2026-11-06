from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import oracledb

app = FastAPI()

# Configuración de CORS para permitir peticiones desde el frontend (HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Credenciales de Oracle actualizadas con el usuario que creaste
DB_USER = "concesionario_user"
DB_PASSWORD = "VentasAuto2026*"
DB_DSN = "localhost:1521/FREEPDB1"

def get_db_connection():
    try:
        return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a Oracle: {str(e)}")

# Modelo de validación de datos
class Auto(BaseModel):
    marca: str
    modelo: str
    anio: int
    precio: float

# --- RUTAS CRUD ---

# 1. LEER (Obtener todos los autos)
@app.get("/autos")
def obtener_autos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, marca, modelo, anio, precio FROM autos ORDER BY id DESC")
    
    autos = [{"id": r[0], "marca": r[1], "modelo": r[2], "anio": r[3], "precio": r[4]} for r in cursor]
    cursor.close()
    connection.close()
    return autos

# 2. CREAR (Registrar un nuevo auto)
@app.post("/autos")
def registrar_auto(auto: Auto):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO autos (marca, modelo, anio, precio) VALUES (:1, :2, :3, :4)",
            [auto.marca, auto.modelo, auto.anio, auto.precio]
        )
        connection.commit()
        return {"mensaje": "Vehículo registrado correctamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# 3. ACTUALIZAR (Modificar un auto existente)
@app.put("/autos/{auto_id}")
def actualizar_auto(auto_id: int, auto: Auto):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE autos SET marca = :1, modelo = :2, anio = :3, precio = :4 WHERE id = :5",
            [auto.marca, auto.modelo, auto.anio, auto.precio, auto_id]
        )
        connection.commit()
        return {"mensaje": "Vehículo actualizado correctamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# 4. ELIMINAR (Borrar un auto del inventario)
@app.delete("/autos/{auto_id}")
def eliminar_auto(auto_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM autos WHERE id = :1", [auto_id])
        connection.commit()
        return {"mensaje": "Vehículo eliminado correctamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()