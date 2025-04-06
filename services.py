from db_connection import connect_to_db
import streamlit as st
import pandas as pd


# Función para obtener las cuentas desde la base de datos
def obtener_cuentas():
    conn = connect_to_db()
    cuentas = []
    if conn:
        try:
            cur = conn.cursor()
            # Consulta SQL para obtener todas las cuentas

            query = """
            SELECT 
                cuenta_id, 
                nombre 
            FROM cuentas 
            ORDER BY 1
            """
            cur.execute(query)
            
            cuentas = cur.fetchall()  # Recuperamos todas las filas con el fetchall, una lista de tuplas
            cur.close()
        
        except Exception as e:
            st.write(f"Error al obtener las cuentas: {e}")
        
        finally:
            conn.close()
    return cuentas

# Funcion para obtener el tipo de cuenta
def obtener_tipo(cuenta_id):
    
    conn = connect_to_db()
    cur = conn.cursor()

    query = """
    SELECT 
        tipo 
    FROM cuentas 
    WHERE cuenta_id = %s
    """
    cur.execute(query,(cuenta_id,))

    tipo_cuenta = cur.fetchone()

    cur.close()
    conn.close()

    if tipo_cuenta:
        return tipo_cuenta[0]
    else:
        return None
    
def obtener_naturaleza(cuenta_id):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT naturaleza FROM cuentas WHERE cuenta_id = %s"
            cur.execute(query, (cuenta_id,))
            result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            st.error(f"Error al obtener la naturaleza de la cuenta {cuenta_id}: {e}")
            return None
        finally:
            conn.close()
    
# Funcion para obtener el saldo de la cuenta
def obtener_saldo(cuenta_id):

    conn = connect_to_db()
    cur = conn.cursor()

    query = """
    SELECT 
        saldo 
    FROM cuentas 
    WHERE cuenta_id = %s    
    """
    cur.execute(query,(cuenta_id,))
    
    saldo_cuenta = cur.fetchone()

    cur.close()
    conn.close()

    if saldo_cuenta:
        return saldo_cuenta[0]
    else:
        return None
    

# Función para realizar la transaccion entre cuentas
def transaccion(cuenta_cargo_id, cuenta_abono_id, monto, descripcion):
    conn = connect_to_db()
    if conn:
        try:
            
            cur = conn.cursor()

             # Verificar si las cuentas existen
            if not obtener_tipo(cuenta_cargo_id) or not obtener_tipo(cuenta_abono_id):
                st.error("Una de las cuentas no existe.")
                return

            tipo_cuenta_cargo = obtener_tipo(cuenta_cargo_id)
            tipo_cuenta_abono = obtener_tipo(cuenta_abono_id)

            naturaleza_cargo = obtener_naturaleza(cuenta_cargo_id)
            naturaleza_abono = obtener_naturaleza(cuenta_abono_id)

            saldo_cargo = obtener_saldo(cuenta_cargo_id)
            saldo_abono = obtener_saldo(cuenta_abono_id)

            # Verificar si hay saldo suficiente en caso de que la transacción reste valor
            if (naturaleza_cargo == 'Acreedora' and monto > saldo_cargo) or \
               (naturaleza_abono == 'Deudora' and monto > saldo_abono):
                st.error("❌ Saldo insuficiente para realizar la transacción.")
                return
            
            # Actualizar saldo de la cuenta cargo
            if naturaleza_cargo == 'Deudora':
                query = "UPDATE cuentas SET saldo = saldo + %s WHERE cuenta_id = %s"
            else:  # Acreedora
                query = "UPDATE cuentas SET saldo = saldo - %s WHERE cuenta_id = %s"
            cur.execute(query, (monto, cuenta_cargo_id))

            # Actualizar saldo de la cuenta abono
            if naturaleza_abono == 'Deudora':
                query = "UPDATE cuentas SET saldo = saldo - %s WHERE cuenta_id = %s"
            else:  # Acreedora
                query = "UPDATE cuentas SET saldo = saldo + %s WHERE cuenta_id = %s"
            cur.execute(query, (monto, cuenta_abono_id))


            # Registrar transacción
            cur.execute(
                "INSERT INTO transacciones(descripcion) VALUES (%s) RETURNING transaccion_id",
                (descripcion,)
            )
            
            # Para recuperar el transaccion_id que se acaba de crear (dato de tipo serial)
            transaccion_id = cur.fetchone()[0]

            # Registrar detalles (Debe - Cargo)
            cur.execute(
                """
                INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto)
                VALUES (%s, %s, 'Debe', %s)
                """,
                (transaccion_id, cuenta_cargo_id, monto)
            )

            # Registrar detalles (Haber - Abono)
            cur.execute(
                """
                INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto)
                VALUES (%s, %s, 'Haber', %s)
                """,
                (transaccion_id, cuenta_abono_id, monto)
            )

            # Commit final
            conn.commit()
            st.success(f"✅ Transacción realizada correctamente.")
 
        except Exception as e:
            conn.rollback()
            st.error(f"❌ Error al realizar la transacción: {e}")
        finally:
            conn.close()

#Función para el estado de situación financiera / Balance general
def get_balance_general():
    conn = connect_to_db()
    if conn:
        try:
            query = """
            WITH utilidades_acumuladas AS (
                SELECT 
                    SUM(CASE WHEN tipo = 'Ingresos' THEN saldo ELSE 0 END) -
                    SUM(CASE WHEN tipo = 'Gastos' THEN saldo ELSE 0 END) AS utilidades
                FROM cuentas
                WHERE tipo IN ('Ingresos', 'Gastos')
            )
            SELECT 
                cuenta_id,
                nombre,
                tipo,
                saldo,
                CASE 
                    WHEN tipo = 'Activo' AND CAST(cuenta_id AS TEXT) ~ '^[12]' THEN 'Activo Corriente'
                    WHEN tipo = 'Activo' AND CAST(cuenta_id AS TEXT) ~ '^3' THEN 'Activo No Corriente'
                    WHEN tipo = 'Pasivo' AND CAST(cuenta_id AS TEXT) ~ '^4' AND cuenta_id NOT IN (45, 49) THEN 'Pasivo Corriente'
                    WHEN tipo = 'Pasivo' AND cuenta_id IN (45, 49) THEN 'Pasivo No Corriente'
                    WHEN tipo = 'Patrimonio' THEN 'Patrimonio'
                END AS categoria
            FROM cuentas
            WHERE saldo <> 0
            
            UNION ALL
            
            SELECT 
                NULL AS cuenta_id, 
                'Utilidades Acumuladas' AS nombre, 
                'Patrimonio' AS tipo, 
                utilidades AS saldo, 
                'Patrimonio' AS categoria
            FROM utilidades_acumuladas
            WHERE utilidades <> 0

            ORDER BY categoria, cuenta_id NULLS LAST;
            """
            
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.write(f"Error al generar el estado de situación financiera: {e}")
        finally:
            conn.close()