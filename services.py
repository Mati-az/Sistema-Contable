from db_connection import connect_to_db
import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

# Obtener fechas automáticas
hoy = date.today()
primer_dia_mes_actual = hoy.replace(day=1)
ultimo_dia_mes_anterior = primer_dia_mes_actual - relativedelta(days=1)
primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

# Para mostrar al usuario
fecha_fin = datetime.combine(hoy, datetime.max.time())
fecha_inicio = datetime.combine(primer_dia_mes_actual, datetime.min.time())
fecha_ultimo_mes = datetime.combine(ultimo_dia_mes_anterior, datetime.max.time())
fecha_corte_anterior = datetime.combine(ultimo_dia_mes_anterior, datetime.max.time())

# Función para obtener las cuentas desde la base de datos
def obtener_cuentas():
    
    conn = connect_to_db()
    cur = conn.cursor()

    cuentas = []

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
    conn.close()
    return cuentas

# Funcion para obtener el tipo de cuenta
def obtener_tipo_cuenta(cuenta_id):
    
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
    
def obtener_naturaleza_cuenta(cuenta_id):
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
    
def get_db_version():
    conn = connect_to_db()
    query = "SELECT COUNT(*) FROM transacciones"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0]


def obtener_saldo_tipo(tipo_cuenta,fecha_inicio='1900-01-01',fecha_fin=None):
    
    if fecha_fin is None:
        fecha_fin = (date.today() + timedelta(days=1)).isoformat()
    
    conn = connect_to_db()
    query = """
    SELECT
        SUM(
            CASE
                WHEN dt.tipo_asiento = 'Debe' AND c.naturaleza = 'Deudora' THEN dt.monto
                WHEN dt.tipo_asiento = 'Haber' AND c.naturaleza = 'Acreedora' THEN dt.monto
                ELSE -dt.monto
            END
        ) AS total
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    JOIN cuentas c ON dt.cuenta_id = c.cuenta_id
    WHERE c.tipo = %s
    AND t.fecha BETWEEN %s AND %s
    GROUP BY c.tipo;
    """
    cur = conn.cursor()
    cur.execute(query,(tipo_cuenta,fecha_inicio,fecha_fin))

    saldo_total = cur.fetchone()

    cur.close()
    conn.close()

    if saldo_total:
        return saldo_total[0]
    else:
        return 0

def obtener_variación(tipo_cuenta, total):

    saldo_hasta_dia_anterior = float(obtener_saldo_tipo(tipo_cuenta,fecha_fin=hoy.isoformat()))

    if saldo_hasta_dia_anterior != 0:
        variacion = (total-saldo_hasta_dia_anterior)/saldo_hasta_dia_anterior
        return variacion
    else:
        return 0

# Función para realizar la transaccion entre cuentas
def transaccion(cuenta_cargo_id, cuenta_abono_id, monto, descripcion):
    conn = connect_to_db()
    if conn:
        try:
            
            cur = conn.cursor()

             # Verificar si las cuentas existen
            if not obtener_tipo_cuenta(cuenta_cargo_id) or not obtener_tipo_cuenta(cuenta_abono_id):
                st.error("Una de las cuentas no existe.")
                return

            naturaleza_cargo = obtener_naturaleza_cuenta(cuenta_cargo_id)
            naturaleza_abono = obtener_naturaleza_cuenta(cuenta_abono_id)

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

# Función para el estado de situación financiera / Balance general
@st.cache_data
def get_balance_general(db_version):
    conn = connect_to_db()
    if conn:
        try:
            query = """
            WITH cuentas_ajustadas AS (
                SELECT
                    cuenta_id,
                    nombre,
                    tipo,
                    -- Ajustar el saldo según la naturaleza
                    CASE 
                        WHEN (tipo IN ('Activo', 'Gastos') AND naturaleza = 'Deudora') OR
                             (tipo IN ('Pasivo', 'Patrimonio', 'Ingresos') AND naturaleza = 'Acreedora')
                        THEN saldo
                        ELSE saldo * -1
                    END AS saldo_ajustado,
                    naturaleza
                FROM cuentas
            ),
            utilidades_acumuladas AS (
                SELECT 
                    SUM(CASE WHEN tipo = 'Ingresos' THEN saldo_ajustado ELSE 0 END) -
                    SUM(CASE WHEN tipo = 'Gastos' THEN saldo_ajustado ELSE 0 END) AS utilidades
                FROM cuentas_ajustadas
                WHERE tipo IN ('Ingresos', 'Gastos')
            )
            SELECT 
                cuenta_id,
                nombre,
                tipo,
                saldo_ajustado AS saldo,
                CASE 
                    WHEN tipo = 'Activo' AND CAST(cuenta_id AS TEXT) ~ '^[12]' THEN 'Activo Corriente'
                    WHEN tipo = 'Activo' AND CAST(cuenta_id AS TEXT) ~ '^3' THEN 'Activo No Corriente'
                    WHEN tipo = 'Pasivo' AND CAST(cuenta_id AS TEXT) ~ '^4' AND cuenta_id NOT IN (45, 49) THEN 'Pasivo Corriente'
                    WHEN tipo = 'Pasivo' AND cuenta_id IN (45, 49) THEN 'Pasivo No Corriente'
                    WHEN tipo = 'Patrimonio' THEN 'Patrimonio'
                END AS categoria
            FROM cuentas_ajustadas
            WHERE saldo_ajustado <> 0

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
            return df
        except Exception as e:
            st.write(f"Error al generar el estado de situación financiera: {e}")
        finally:
            conn.close()


def calcular_estado_resultados():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()

            # Ingresos: sumamos todas las cuentas de tipo 'Ingresos'
            cur.execute("""
                SELECT nombre, saldo 
                FROM cuentas 
                WHERE tipo = 'Ingresos'
            """)
            ingresos_rows = cur.fetchall()
            total_ingresos = sum(row[1] for row in ingresos_rows)

            # Gastos: sumamos todas las cuentas de tipo 'Gastos'
            cur.execute("""
                SELECT nombre, saldo 
                FROM cuentas 
                WHERE tipo = 'Gastos'
            """)
            gastos_rows = cur.fetchall()
            total_gastos = sum(row[1] for row in gastos_rows)

            utilidad_neta = total_ingresos - total_gastos

            return {
                "ingresos": ingresos_rows,
                "gastos": gastos_rows,
                "total_ingresos": total_ingresos,
                "total_gastos": total_gastos,
                "utilidad_neta": utilidad_neta
            }

        except Exception as e:
            st.error(f"Error al calcular estado de resultados: {e}")
        finally:
            conn.close()

def calcular_estado_capital():
    # Función para ejecutar query
    def obtener_dato(query, params=None):
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchone()
                return result[0] if result else 0

    # Consultas
    capital_inicial_query = """
    SELECT COALESCE(SUM(CASE 
        WHEN dt.tipo_asiento = 'Haber' THEN dt.monto 
        ELSE -dt.monto END), 0)
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    WHERE dt.cuenta_id = 50 AND t.fecha <= %s;
    """

    inversiones_query = """
    SELECT COALESCE(SUM(dt.monto), 0)
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    WHERE dt.cuenta_id = 50 AND dt.tipo_asiento = 'Haber'
    AND t.fecha BETWEEN %s AND %s;
    """

    retiros_query = """
    SELECT COALESCE(SUM(dt.monto), 0)
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    WHERE dt.cuenta_id = 50 AND dt.tipo_asiento = 'Debe'
    AND t.fecha BETWEEN %s AND %s;
    """

    ingresos_query = """
    SELECT COALESCE(SUM(CASE 
        WHEN dt.tipo_asiento = 'Haber' THEN dt.monto 
        ELSE -dt.monto END), 0)
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    JOIN cuentas c ON dt.cuenta_id = c.cuenta_id
    WHERE c.tipo = 'Ingresos' AND t.fecha BETWEEN %s AND %s;
    """

    gastos_query = """
    SELECT COALESCE(SUM(CASE 
        WHEN dt.tipo_asiento = 'Debe' THEN dt.monto 
        ELSE -dt.monto END), 0)
    FROM detalles_transacciones dt
    JOIN transacciones t ON dt.transaccion_id = t.transaccion_id
    JOIN cuentas c ON dt.cuenta_id = c.cuenta_id
    WHERE c.tipo = 'Gastos' AND t.fecha BETWEEN %s AND %s;
    """

    # Obtener valores
    capital_inicial = obtener_dato(capital_inicial_query, (fecha_ultimo_mes,))
    inversiones = obtener_dato(inversiones_query, (fecha_inicio, fecha_fin))
    retiros = obtener_dato(retiros_query, (fecha_inicio, fecha_fin))
    ingresos = obtener_dato(ingresos_query, (fecha_inicio, fecha_fin))
    gastos = obtener_dato(gastos_query, (fecha_inicio, fecha_fin))
    utilidad_neta = ingresos - gastos
    capital_final = capital_inicial + inversiones + utilidad_neta - retiros

    # Retornar todos los valores
    return {
        'capital_inicial': capital_inicial,
        'inversiones': inversiones,
        'retiros': retiros,
        'ingresos': ingresos,
        'gastos': gastos,
        'utilidad_neta': utilidad_neta,
        'capital_final': capital_final
    }

def obtener_saldo_cuenta(tipo_cuenta):
    conn = connect_to_db()
    if conn:
        try:
            query = """
                SELECT 
                    c.cuenta_id,
                    c.nombre,
                    c.tipo,
                    c.naturaleza,
                    COALESCE(SUM(
                        CASE 
                            WHEN c.naturaleza = 'Deudora' AND dt.tipo_asiento = 'Debe' THEN dt.monto
                            WHEN c.naturaleza = 'Deudora' AND dt.tipo_asiento = 'Haber' THEN -dt.monto
                            WHEN c.naturaleza = 'Acreedora' AND dt.tipo_asiento = 'Haber' THEN dt.monto
                            WHEN c.naturaleza = 'Acreedora' AND dt.tipo_asiento = 'Debe' THEN -dt.monto
                            ELSE 0
                        END
                    ), 0) AS saldo
                FROM cuentas c
                LEFT JOIN detalles_transacciones dt ON c.cuenta_id = dt.cuenta_id
                WHERE c.tipo = %s
                GROUP BY c.cuenta_id, c.nombre, c.tipo, c.naturaleza
                HAVING saldo != 0
                ORDER BY c.cuenta_id;
            """
            
            df = pd.read_sql(query, conn, params=(tipo_cuenta,))
            df = df.reset_index(drop=True)
            return df
        except Exception as e:
            print(f"Error al obtener los saldos de las cuentas: {e}")
            return None
        finally:
            conn.close()