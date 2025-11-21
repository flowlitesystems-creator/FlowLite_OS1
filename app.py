import sqlite3
import csv
from datetime import datetime
from config import DB_NAME


# ============================================================
#  CONEXIÓN A BASE DE DATOS
# ============================================================

def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre
    return conn


# ============================================================
#  CREAR TABLA SI NO EXISTE
# ============================================================

def inicializar_db():
    conn = conectar_db()
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
#  REGISTRAR CLIENTE
# ============================================================

def registrar_cliente(nombre, telefono, origen):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nombre, telefono, origen, fecha)
        VALUES (?, ?, ?, ?)
    """, (nombre, telefono, origen, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    return True


# ============================================================
#  LISTAR CLIENTES
# ============================================================

def listar_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "nombre": r["nombre"],
            "telefono": r["telefono"],
            "origen": r["origen"],
            "fecha": r["fecha"]
        }
        for r in rows
    ]


# ============================================================
#   BUSCAR POR NOMBRE
# ============================================================

def buscar_por_nombre(nombre):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ?", (f"%{nombre}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================
#   BUSCAR POR TELÉFONO
# ============================================================

def buscar_por_telefono(telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefono LIKE ?", (f"%{telefono}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================
#   BUSCAR POR ORIGEN
# ============================================================

def buscar_por_origen(origen):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE origen LIKE ?", (f"%{origen}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================
#   ACTUALIZAR CLIENTE
# ============================================================

def actualizar_cliente(id_cliente, nombre, telefono, origen):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, telefono = ?, origen = ?
        WHERE id = ?
    """, (nombre, telefono, origen, id_cliente))

    conn.commit()
    cambiado = cursor.rowcount > 0
    conn.close()
    return cambiado


# ============================================================
#   ELIMINAR CLIENTE
# ============================================================

def eliminar_cliente(id_cliente):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()
    return True


# ============================================================
#  CONTAR CLIENTES
# ============================================================

def contar_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM clientes")
    total = cursor.fetchone()["total"]
    conn.close()
    return total


# ============================================================
#  EXPORTAR A CSV
# ============================================================

def exportar_csv(nombre_archivo="clientes_exportados.csv"):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    conn.close()

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Nombre", "Telefono", "Origen", "Fecha"])

        for r in rows:
            writer.writerow([
                r["id"],
                r["nombre"],
                r["telefono"],
                r["origen"],
                r["fecha"]
            ])

    return True


# ============================================================
#  IMPORTAR DESDE CSV
# ============================================================

def importar_csv(nombre_archivo):
    conn = conectar_db()
    cursor = conn.cursor()

    with open(nombre_archivo, "r", encoding="utf-8") as csvfile:
        for linea in csvfile.readlines()[1:]:  # evitar encabezado
            campos = linea.strip().split(",")

            if len(campos) < 5:
                continue

            _, nombre, telefono, origen, fecha = campos

            cursor.execute("""
                INSERT INTO clientes (nombre, telefono, origen, fecha)
                VALUES (?, ?, ?, ?)
            """, (nombre, telefono, origen, fecha))

    conn.commit()
    conn.close()
    return True


# ============================================================
#  INICIO DIRECTO
# ============================================================

if __name__ == "__main__":
    inicializar_db()
    print("FlowLite OS 1.0 iniciado correctamente.")
