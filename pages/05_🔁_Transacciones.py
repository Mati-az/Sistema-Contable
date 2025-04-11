import streamlit as st
from services import obtener_cuentas, transaccion
import pandas as pd
from datetime import datetime, timedelta
from db_connection import connect_to_db

st.set_page_config(page_title="Registro de Transacciones", page_icon="🔁", layout="wide")

st.title("🔁 Transacciones")
st.write("""
    💬 Aquí puedes **registrar nuevas operaciones contables** y consultar el **historial** de movimientos financieros de tu empresa.
    
    🔄 Cada transacción incluye la cuenta de cargo, la cuenta de abono, el monto y una descripción detallada.
    
    📊 Usa esta sección para mantener el control preciso y organizado de tu contabilidad diaria.
""")

st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
st.write("### 📒 **Registro de Transacciones**")

st.markdown(
    """
    <style>

        section[data-testid="stSidebar"] {
            background-color: #dbeafe;
        }

        [data-testid="stSidebarNav"] a {
            color: #111827 !important;
        }

        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNav"] a:focus,
        [data-testid="stSidebarNav"] a:active,
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #93c5fd !important;
            color: #111827 !important;
            font-weight: bold;
            border-radius: 10px;
            margin: 0px 25px;
            padding: 0px 5px;
            
            display: flex;
            align-items: center;
            gap: 10px; /* espacio entre ícono y texto */
            text-decoration: none;
        }

        [data-testid="stSidebarNav"]::before {
            content: "🖥️ Dashboard";
            display: block;
            margin-left: 20px;
            margin-bottom: 15px;
            font-size: 30px;
            font-weight: 700;
            color: #111827;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Obtener las cuentas de la base de datos
cuentas = obtener_cuentas()

lista_cuentas = [f"{cuenta[0]} - {cuenta[1]}" for cuenta in cuentas]

# Crear una caja de selección para la cuenta de cargo y abono
col1, col2, col3 = st.columns([2,1,2])

with col1:
    cuenta_cargo = st.selectbox("Cuenta de Cargo", lista_cuentas, help="La cuenta que será **debitada** en la transacción.")
with col2:
    monto = st.number_input("Monto de la transacción", min_value=1, step=100)    
with col3:
    cuenta_abono = st.selectbox("Cuenta de Abono", lista_cuentas, help="La cuenta que será **acreditada** en la transacción.")

descripcion_transaccion = st.text_area("Descripción de la transacción")
    
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

st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)

st.write("### 📜 **Historial de Transacciones**")

# Opciones de filtro de tiempo
filtro = st.selectbox("📅 Ver transacciones de:", 
                    ["Hoy", "Últimos 7 días", "Últimos 30 días", "Personalizado"])

# Calcular el rango de fechas según opción
fecha_fin = datetime.today()
if filtro == "Hoy":
    fecha_ini = fecha_fin.replace(hour=0, minute=0, second=0, microsecond=0)
elif filtro == "Últimos 7 días":
    fecha_ini = fecha_fin - timedelta(days=7)
elif filtro == "Últimos 30 días":
    fecha_ini = fecha_fin - timedelta(days=30)
else:
# Rango personalizado con date_input
    c1, c2 = st.columns(2)
    with c1:
        fecha_ini = st.date_input("Desde", value=fecha_fin - timedelta(days=7))
    with c2:
        fecha_fin = st.date_input("Hasta", value=fecha_fin)

query = """
SELECT 
    t.fecha AS "Fecha de Transacción",
    c.nombre AS "Cuenta",
    t.descripcion AS "Descripción", 
    dt.tipo_asiento AS "Tipo de Asiento", 
    dt.monto AS "Monto (S/.)"
FROM transacciones t
JOIN detalles_transacciones dt ON t.transaccion_id = dt.transaccion_id
JOIN cuentas c ON dt.cuenta_id = c.cuenta_id
WHERE t.fecha BETWEEN %s AND %s
ORDER BY t.fecha DESC
"""
conn = connect_to_db()
df = pd.read_sql(query, conn, params=(fecha_ini, fecha_fin))
df["Monto (S/.)"] = df["Monto (S/.)"].apply(lambda x: f"S/. {x:,.2f}" if pd.notnull(x) else "")
df = df.reset_index(drop=True)

if st.button("Ver Historial"):
    st.markdown("### 📄 Transacciones registradas")
    st.dataframe(df, use_container_width=True)    
