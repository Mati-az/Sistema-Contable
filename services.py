from db_connection import connect_to_db
import streamlit as st


# Función para obtener las cuentas desde la base de datos
def obtener_cuentas():
    conn = connect_to_db()
    cuentas = []
    if conn:
        try:
            cur = conn.cursor()
            # Consulta SQL para obtener todas las cuentas
            cur.execute("SELECT cuenta_id, nombre FROM cuentas ORDER BY 1")
            cuentas = cur.fetchall()  # Recuperamos todas las filas
            cur.close()
        except Exception as e:
            st.write(f"Error al obtener las cuentas: {e}")
        finally:
            conn.close()
    return cuentas

def transaccion(diccionario_cargo, diccionario_abono, monto, descripcion):
    conn = connect_to_db()
    if conn:
        try:
            
            cur = conn.cursor()

            # Obtenemos el tipo de cuenta de la cuenta cargo y abono
            cur.execute("SELECT tipo FROM CUENTAS WHERE cuenta_id = %s", (diccionario_cargo["cuenta_id"],))
            tipo_cuenta_cargo = cur.fetchone()
            
            if tipo_cuenta_cargo:
                tipo_cuenta_cargo = tipo_cuenta_cargo[0]

            cur.execute("SELECT tipo FROM CUENTAS WHERE cuenta_id = %s", (diccionario_abono["cuenta_id"],))
            tipo_cuenta_abono = cur.fetchone()

            if tipo_cuenta_abono:
                tipo_cuenta_abono = tipo_cuenta_abono[0]


            # Verificamos si existe saldo suficiente en la cuenta que se le va a restar el monto
            # Si se trata de la cuenta cargo este solo se restara si se trata del pasivo, patrimonio o ingresos
            # Si se trata de la cuenta abono este solo se restara si se trata del activo o gasto

            if tipo_cuenta_cargo == "Pasivo" or tipo_cuenta_cargo == "Patrimonio" or tipo_cuenta_cargo == "Ingresos":
                cur.execute("SELECT saldo FROM CUENTAS WHERE cuenta_id = %s", (diccionario_cargo["cuenta_id"],))
                saldo_cuenta_cargo = cur.fetchone()
                
                # Acceder al primer valor de la tupla
                if saldo_cuenta_cargo:
                    saldo_cuenta_cargo = saldo_cuenta_cargo[0]

                if monto > saldo_cuenta_cargo:
                    st.error(f"Error! revisar la cuenta {diccionario_cargo["cuenta_id"]}: {diccionario_cargo["nombre_cuenta"]}" )
                    return
                
            if tipo_cuenta_abono == "Activo" or tipo_cuenta_abono == "Gastos":
                cur.execute("SELECT saldo FROM CUENTAS WHERE cuenta_id = %s", (diccionario_abono["cuenta_id"],))
                saldo_cuenta_abono = cur.fetchone()

                if saldo_cuenta_abono:
                    saldo_cuenta_abono = saldo_cuenta_abono[0]
          
                if monto > saldo_cuenta_abono:
                    st.error(f"Saldo insuficiente en la cuenta {diccionario_abono["cuenta_id"]}: {diccionario_abono["nombre_cuenta"]}")
                    return
            
            # Actualizamos el saldo de la cuenta cargo
            if tipo_cuenta_cargo == "Activo" or tipo_cuenta_cargo == "Gastos":
                cur.execute("UPDATE cuentas SET saldo = saldo + %s WHERE cuenta_id = %s", (monto, diccionario_cargo["cuenta_id"],))
            else:
                cur.execute("UPDATE cuentas SET saldo = saldo - %s WHERE cuenta_id = %s", (monto, diccionario_cargo["cuenta_id"],))

            # Actualizacmos el saldo de la cuenta abono
            if tipo_cuenta_abono == "Activo" or tipo_cuenta_abono == "Gastos":
                cur.execute("UPDATE cuentas SET saldo = saldo - %s WHERE cuenta_id = %s", (monto, diccionario_abono["cuenta_id"],))
            else:
                cur.execute("UPDATE cuentas SET saldo = saldo + %s WHERE cuenta_id = %s", (monto, diccionario_abono["cuenta_id"],))

            # Registramos la transacción
            cur.execute("INSERT INTO transacciones(descripcion) VALUES (%s) RETURNING transaccion_id", (descripcion,))
            transaccion_id = cur.fetchone()[0]
            conn.commit()

            # Registramos la cuenta cargo
            cur.execute("INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto) VALUES (%s,%s,'Debe',%s)", (transaccion_id, diccionario_cargo["cuenta_id"], monto,))
            conn.commit()

            #Registramos la cuenta abono
            cur.execute("INSERT INTO detalles_transacciones(transaccion_id, cuenta_id, tipo_asiento, monto) VALUES (%s,%s,'Haber',%s)", (transaccion_id, diccionario_abono["cuenta_id"], monto,))
            conn.commit()

            st.success(f"✅ Transacción realizada correctamente")
 
        except Exception as e:
            st.write(f"Error al realizar la transaccion: {e}")
        finally:
            conn.close()