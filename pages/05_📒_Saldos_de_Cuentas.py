import streamlit as st
from services import obtener_saldos_cuentas

st.set_page_config(page_title="Saldos de Cuentas", layout="wide")

st.title("📒 Saldos de las Cuentas")

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


