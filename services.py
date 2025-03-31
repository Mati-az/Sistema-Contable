from db_connection import connect_to_db

# Función para obtener las cuentas desde la base de datos
def obtener_cuentas():
    conn = connect_to_db()
    cuentas = []
    if conn:
        try:
            cur = conn.cursor()
            # Consulta SQL para obtener todas las cuentas
            cur.execute("SELECT cuenta_id, nombre FROM cuentas")
            cuentas = cur.fetchall()  # Recuperamos todas las filas
            cur.close()
        except Exception as e:
            print(f"Error al obtener las cuentas: {e}")
        finally:
            conn.close()
    return cuentas