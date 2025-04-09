import streamlit as st
from services import obtener_cuentas, transaccion

# Titulo
st.title("🔄Transacciones")

# Obtener las cuentas de la base de datos
cuentas = obtener_cuentas()

lista_cuentas = [f"{cuenta[0]} - {cuenta[1]}" for cuenta in cuentas]

# Crear una caja de selección para la cuenta de cargo y abono


col1, col2, = st.columns(2)

with col1:
    cuenta_cargo = st.selectbox("Cuenta de Cargo", lista_cuentas)
with col2:
    cuenta_abono = st.selectbox("Cuenta de Abono", lista_cuentas)
    
descripcion_transaccion = st.text_area("Descripción de la transacción", "")
monto = st.number_input("Monto de la transacción", min_value=1, step=100)

# Recuperar el codigo de las cuentas
if cuenta_cargo:
    cuenta_cargo_id = int(cuenta_cargo.split(' - ')[0])

if cuenta_abono:
    cuenta_abono_id = int(cuenta_abono.split(' - ')[0])

# Boton para la transacción
if st.button("Realizar Transacción"):
    if cuenta_cargo_id != cuenta_abono_id:
                
        transaccion(cuenta_cargo_id, cuenta_abono_id, monto, descripcion_transaccion)

    else:
        st.warning("⚠️ Transacción invalida: Ingrese dos cuentas diferentes")