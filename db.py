import sqlite3
from config import DB_NAME


# ============================================================
#  CONEXIÓN A BASE DE DATOS
# ============================================================

def get_connection():
    """
    Retorna una conexión activa a la base de datos.
    row_factory permite tratar los registros como diccionarios.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
#  CREAR TABLAS Si NO EXISTEN
# ============================================================

def init_db():
    """
    Inicializa la base de datos y crea las tablas necesarias
    para FlowLite OS 1.0.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            origen TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
#  UTILIDAD PARA CONSULTAS SELECT
# ============================================================

def query_all(sql, params=()):
    """
    Ejecuta una consulta SELECT y retorna todas las filas.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_one(sql, params=()):
    """
    Ejecuta una consulta SELECT y retorna una sola fila.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ============================================================
#  UTILIDAD PARA INSERT / UPDATE / DELETE
# ============================================================

def execute(sql, params=()):
    """
    Ejecuta una operación de escritura y retorna True si hubo
    cambios reales en la base de datos.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    cambios = cursor.rowcount > 0
    conn.close()
    return cambios
