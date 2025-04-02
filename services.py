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

            tipo_cuenta_cargo = obtener_tipo(cuenta_cargo_id)
            tipo_cuenta_abono = obtener_tipo(cuenta_abono_id)

            # Verificamos si existe saldo suficiente en la cuenta que se le va a restar el monto
            # Si se trata de la cuenta cargo este solo se restara si se trata del pasivo, patrimonio o ingresos
            # Si se trata de la cuenta abono este solo se restara si se trata del activo o gasto

            if tipo_cuenta_cargo == "Pasivo" or tipo_cuenta_cargo == "Patrimonio" or tipo_cuenta_cargo == "Ingresos":

                saldo_cuenta_cargo = obtener_saldo(cuenta_cargo_id)

                # si el monto es mayor que el saldo disponible accede al error
                if monto > saldo_cuenta_cargo:
                    st.error(f"Error! revisar la cuenta {cuenta_cargo_id}" )
                    return
                
            if tipo_cuenta_abono == "Activo" or tipo_cuenta_abono == "Gastos":
            
                saldo_cuenta_abono = obtener_saldo(cuenta_abono_id)
          
                # si el monto es mayor que el saldo disponible accede al error
                if monto > saldo_cuenta_abono:
                    st.error(f"Saldo insuficiente en la cuenta {cuenta_abono_id}")
                    return
            
            # Actualizamos el saldo de la cuenta cargo
            if tipo_cuenta_cargo == "Activo" or tipo_cuenta_cargo == "Gastos":

                query = """
                UPDATE cuentas 
                SET saldo = saldo + %s 
                WHERE cuenta_id = %s
                """
                cur.execute(query, (monto, cuenta_cargo_id,))

            else:

                query = """
                UPDATE cuentas 
                SET saldo = saldo - %s 
                WHERE cuenta_id = %s
                """
                cur.execute(query, (monto, cuenta_cargo_id,))

            # Actualizacmos el saldo de la cuenta abono
            if tipo_cuenta_abono == "Activo" or tipo_cuenta_abono == "Gastos":

                query = """
                UPDATE cuentas 
                SET saldo = saldo - %s 
                WHERE cuenta_id = %s
                """
                cur.execute(query, (monto, cuenta_abono_id,))

            else:

                query = """
                UPDATE cuentas 
                SET saldo = saldo + %s 
                WHERE cuenta_id = %s
                """
                cur.execute(query, (monto, cuenta_abono_id,))

            # Registramos la transacción
            
            query = """
            INSERT INTO transacciones(descripcion) 
            VALUES (%s) 
            RETURNING transaccion_id
            """
            cur.execute(query, (descripcion,))
            
            # Para recuperar el transaccion_id que se acaba de crear (dato de tipo serial)
            transaccion_id = cur.fetchone()[0]
            conn.commit()

            # Registramos la cuenta cargo
            
            query = """
            INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto) 
            VALUES (%s,%s,'Debe',%s)
            """
            cur.execute(query, (transaccion_id, cuenta_cargo_id, monto,))
            conn.commit()

            #Registramos la cuenta abono

            query = """
            INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto) 
            VALUES (%s,%s,'Haber',%s)
            """
            cur.execute(query, (transaccion_id, cuenta_abono_id, monto,))
            conn.commit()

            st.success(f"✅ Transacción realizada correctamente")
 
        except Exception as e:
            st.write(f"Error al realizar la transaccion: {e}")
        finally:
            conn.close()
