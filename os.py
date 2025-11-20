import os
from datetime import datetime, timedelta
from app import (
    registrar_cliente,
    listar_clientes,
    buscar_por_nombre,
    buscar_por_telefono,
    buscar_por_origen,
    actualizar_cliente,
    eliminar_cliente,
    exportar_csv,
    importar_csv,
    contar_clientes,
)

# ============================================================
#               UTILIDADES BÁSICAS
# ============================================================

def limpiar():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


# ============================================================
#               MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    print("""
===========================================
           FLOWLITE OS 1.0
===========================================

1. Registrar cliente
2. Listar clientes
3. Buscar por nombre
4. Buscar por teléfono
5. Buscar por origen
6. Actualizar cliente
7. Eliminar cliente
8. Exportar a CSV
9. Importar desde CSV
10. Contar clientes
11. Ver dashboard

0. Salir

===========================================
""")


# ============================================================
#               ACCIONES DEL MENÚ
# ============================================================

def opcion_registrar():
    limpiar()
    print("=== Registrar cliente ===\n")
    nombre = input("Nombre   : ").strip()
    telefono = input("Teléfono : ").strip()
    origen = input("Origen   : ").strip()

    registrar_cliente(nombre, telefono, origen)
    print("\nCliente registrado correctamente.")
    pausar()


def opcion_listar():
    limpiar()
    print("=== Lista de clientes ===\n")
    clientes = listar_clientes()

    if not clientes:
        print("(No hay clientes registrados)")
    else:
        for c in clientes:
            print(f"[{c['id']}] {c['nombre']} | {c['telefono']} | {c['origen']} | {c['fecha']}")

    pausar()


def opcion_buscar_nombre():
    limpiar()
    print("=== Buscar por nombre ===\n")
    nombre = input("Nombre o parte del nombre: ").strip()

    resultados = buscar_por_nombre(nombre)
    if not resultados:
        print("\n(No se encontraron coincidencias)")
    else:
        for r in resultados:
            print(f"[{r['id']}] {r['nombre']} | {r['telefono']} | {r['origen']} | {r['fecha']}")

    pausar()


def opcion_buscar_telefono():
    limpiar()
    print("=== Buscar por teléfono ===\n")
    telefono = input("Teléfono o parte del teléfono: ").strip()

    resultados = buscar_por_telefono(telefono)
    if not resultados:
        print("\n(No se encontraron coincidencias)")
    else:
        for r in resultados:
            print(f"[{r['id']}] {r['nombre']} | {r['telefono']} | {r['origen']} | {r['fecha']}")

    pausar()


def opcion_buscar_origen():
    limpiar()
    print("=== Buscar por origen ===\n")
    origen = input("Origen (ej: Instagram, WhatsApp, TikTok): ").strip()

    resultados = buscar_por_origen(origen)
    if not resultados:
        print("\n(No se encontraron coincidencias)")
    else:
        for r in resultados:
            print(f"[{r['id']}] {r['nombre']} | {r['telefono']} | {r['origen']} | {r['fecha']}")

    pausar()


def opcion_actualizar():
    limpiar()
    print("=== Actualizar cliente ===\n")
    id_cliente = input("ID del cliente a actualizar: ").strip()

    print("\nIngrese los NUEVOS datos (se reemplazarán los actuales):\n")
    nuevo_nombre = input("Nuevo nombre   : ").strip()
    nuevo_telefono = input("Nuevo teléfono : ").strip()
    nuevo_origen = input("Nuevo origen   : ").strip()

    ok = actualizar_cliente(id_cliente, nuevo_nombre, nuevo_telefono, nuevo_origen)
    if ok:
        print("\nCliente actualizado correctamente.")
    else:
        print("\nNo se encontró un cliente con ese ID.")

    pausar()


def opcion_eliminar():
    limpiar()
    print("=== Eliminar cliente ===\n")
    id_cliente = input("ID del cliente a eliminar: ").strip()

    confirmar = input(f"¿Seguro que deseas eliminar el cliente {id_cliente}? (s/n): ").strip().lower()
    if confirmar == "s":
        eliminar_cliente(id_cliente)
        print("\nCliente eliminado.")
    else:
        print("\nAcción cancelada.")

    pausar()


def opcion_exportar():
    limpiar()
    print("=== Exportar a CSV ===\n")
    nombre_archivo = input("Nombre del archivo (Enter = clientes_exportados.csv): ").strip()
    if not nombre_archivo:
        nombre_archivo = "clientes_exportados.csv"

    exportar_csv(nombre_archivo)
    print(f"\nArchivo '{nombre_archivo}' exportado correctamente.")
    pausar()


def opcion_importar():
    limpiar()
    print("=== Importar desde CSV ===\n")
    nombre_archivo = input("Nombre del archivo CSV: ").strip()

    importar_csv(nombre_archivo)
    print("\nDatos importados correctamente.")
    pausar()


def opcion_contar():
    limpiar()
    print("=== Total de clientes ===\n")
    total = contar_clientes()
    print(f"Total registrados: {total}")
    pausar()


def opcion_dashboard():
    limpiar()
    print("=== Dashboard FlowLite OS 1.0 ===\n")

    clientes = listar_clientes()
    if not clientes:
        print("No hay clientes registrados aún.")
        pausar()
        return

    total = len(clientes)
    hoy = datetime.now().date()
    hace_7_dias = hoy - timedelta(days=7)

    clientes_hoy = 0
    clientes_ultimos_7 = 0
    origen_counts = {}
    fechas_con_clientes = []  # lista de (datetime, cliente)

    for c in clientes:
        # origen
        origen = c.get("origen", "Sin origen")
        origen_counts[origen] = origen_counts.get(origen, 0) + 1

        # fecha
        try:
            f = datetime.strptime(c["fecha"], "%Y-%m-%d %H:%M:%S")
            fechas_con_clientes.append((f, c))

            if f.date() == hoy:
                clientes_hoy += 1
            if hace_7_dias <= f.date() <= hoy:
                clientes_ultimos_7 += 1
        except Exception:
            # si alguna fecha viene mal, la ignoramos
            continue

    fechas_con_clientes.sort(key=lambda x: x[0])
    primer_registro = fechas_con_clientes[0][0] if fechas_con_clientes else None
    ultimo_registro = fechas_con_clientes[-1][0] if fechas_con_clientes else None

    print(f"Total de clientes           : {total}")
    print(f"Clientes registrados hoy    : {clientes_hoy}")
    print(f"Registros últimos 7 días    : {clientes_ultimos_7}")

    if primer_registro:
        print(f"Primer registro             : {primer_registro.strftime('%Y-%m-%d %H:%M:%S')}")
    if ultimo_registro:
        print(f"Último registro             : {ultimo_registro.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n--- Clientes por origen ---")
    for origen, cant in origen_counts.items():
        print(f"- {origen}: {cant}")

    print("\n--- Últimos 5 clientes ---")
    ultimos_5 = sorted(fechas_con_clientes, key=lambda x: x[0], reverse=True)[:5]
    for f, c in ultimos_5:
        print(f"{f.strftime('%Y-%m-%d %H:%M:%S')} | {c['nombre']} | {c['telefono']} | {c['origen']}")

    pausar()


# ============================================================
#               LOOP PRINCIPAL
# ============================================================

def main():
    while True:
        limpiar()
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_registrar()
        elif opcion == "2":
            opcion_listar()
        elif opcion == "3":
            opcion_buscar_nombre()
        elif opcion == "4":
            opcion_buscar_telefono()
        elif opcion == "5":
            opcion_buscar_origen()
        elif opcion == "6":
            opcion_actualizar()
        elif opcion == "7":
            opcion_eliminar()
        elif opcion == "8":
            opcion_exportar()
        elif opcion == "9":
            opcion_importar()
        elif opcion == "10":
            opcion_contar()
        elif opcion == "11":
            opcion_dashboard()
        elif opcion == "0":
            limpiar()
            print("Cerrando FlowLite OS 1.0...")
            break
        else:
            print("\nOpción inválida.")
            pausar()


if __name__ == "__main__":
    main()
