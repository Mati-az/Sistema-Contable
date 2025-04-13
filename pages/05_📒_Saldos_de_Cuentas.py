import streamlit as st
from services import obtener_saldos_cuentas

st.set_page_config(page_title="Saldos de Cuentas", layout="wide")

st.title("📒 Saldos de las Cuentas")

# Obtener datos
saldos_df = obtener_saldos_cuentas()

if saldos_df.empty:
    st.warning("No se encontraron datos.")
else:
    # Mostrar en 3 columnas
    col1, col2, col3 = st.columns(3)

    for idx, row in saldos_df.iterrows():
        cuenta_id = row['cuenta_id']
        nombre = row['nombre']
        tipo = row['tipo']
        naturaleza = row['naturaleza']
        saldo = row['saldo']

        if idx % 3 == 0:
            container = col1
        elif idx % 3 == 1:
            container = col2
        else:
            container = col3

        with container:
            if saldo == 0:
                saldo_texto = "<span style='color:gray;'>-</span>"
            elif saldo > 0:
                saldo_texto = f"<span style='color:green;'>S/ {saldo:,.2f}</span>"
            else:
                saldo_texto = f"<span style='color:red;'>S/ {saldo:,.2f}</span>"

            label = f"**{cuenta_id} {nombre} ({naturaleza})**"

            st.markdown(f"""
                {label}<br>
                {saldo_texto}
            """, unsafe_allow_html=True)


