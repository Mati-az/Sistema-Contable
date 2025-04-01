import streamlit as st
from services import obtener_cuentas

def main():

    # Titulo
    st.title("Sistema Contable")

    # Obtener las cuentas de la base de datos
    cuentas = obtener_cuentas()

    lista_cuentas = [f"{cuenta[0]} - {cuenta[1]}" for cuenta in cuentas]

    # Crear una caja de selección para la cuenta de cargo
    cuenta_cargo = st.selectbox("Cuenta de Cargo", lista_cuentas)

    if cuenta_cargo:
        cuenta_id = int(cuenta_cargo.split(' - ')[0])  # Obtener cuenta_id
        nombre_cuenta = cuenta_cargo.split(' - ')[1]  # Obtener nombre de la cuenta

        # Guardar los valores como un diccionario
        diccionario_cargo = {
            "cuenta_id": cuenta_id,
            "nombre_cuenta": nombre_cuenta
        }

    # Crear una caja de selección para la cuenta de abono
    cuenta_abono = st.selectbox("Cuenta de Abono", lista_cuentas)

    if cuenta_abono:
        cuenta_id = int(cuenta_abono.split(' - ')[0])  # Obtener cuenta_id
        nombre_cuenta = cuenta_abono.split(' - ')[1]  # Obtener nombre de la cuenta

        # Guardar los valores como un diccionario
        diccionario_abono = {
            "cuenta_id": cuenta_id,
            "nombre_cuenta": nombre_cuenta
        }

    monto = st.number_input("Monto de la transacción", min_value=1, step=50)

    if st.button("Realizar Transacción"):
            if diccionario_cargo["cuenta_id"] != diccionario_abono["cuenta_id"]:
                
                #falta implemetar la logica de la transaccion
                st.success(f"✅ Transacción realizada correctamente, monto: {monto}")

            else:
                st.warning("⚠️ Transacción invalida: Ingrese dos cuentas diferentes")

if __name__ == "__main__":
    main()

#Para correr la aplicación poner en el terminal: streamlit run app.py