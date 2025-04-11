import streamlit as st
from services import obtener_saldo_total, obtener_variación_hasta_ayer
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Sistema Contable", page_icon="📊", layout="wide")

st.title("📊 Bienvenido al Sistema Contable")
st.write("""
👋 **¡Bienvenido al Sistema Contable!**  

Este sistema ha sido diseñado para brindarte una **gestión financiera eficiente, ordenada y visual**.  
Aquí podrás:

✅ **Registrar transacciones** contables de forma rápida y segura.  
📊 **Consultar balances** actualizados por periodo: activos, pasivos, ingresos y gastos.  
📂 **Visualizar reportes** interactivos para tomar decisiones informadas.  
⚙️ **Configurar tus cuentas** y personalizar la operación según tu necesidad.

Todo lo que necesitas para tener el **control total de tu contabilidad**, en una sola plataforma.
""")

st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)


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

st.markdown("### 🧮 Resumen Financiero Mensual")
st.write("Visualiza el total de activos, pasivos, ingresos y gastos junto con su variación porcentual respecto al total hasta el dia anterior.")
st.write("")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,1,2,1,2,1,2])

with col1:
    st.image("imagenes/activos.png", width=110)

with col2:
    total_activo = float(obtener_saldo_total("Activo"))
    var_activo = float(obtener_variación_hasta_ayer("Activo",total_activo))

    st.metric(label="ACTIVOS TOTALES", value=total_activo, delta=f"{var_activo:.2f}%", help = None)

with col3:
    st.image("imagenes/pasivos.png", width=110)

with col4:
    total_pasivo = float(obtener_saldo_total("Pasivo"))
    var_pasivo = float(obtener_variación_hasta_ayer("Pasivo",total_pasivo))

    st.metric(label="PASIVOS TOTALES", value=total_pasivo, delta=f"{var_pasivo:.2f}%", help = None)

with col5:
    st.image("imagenes/ingresos.png", width=110)

with col6:
    total_ingresos = float(obtener_saldo_total("Ingresos"))
    var_ingresos = float(obtener_variación_hasta_ayer("Ingresos",total_ingresos))

    st.metric(label="INGRESOS TOTALES", value=total_ingresos, delta=f"{var_ingresos:.2f}%",help=None)

with col7:
    st.image("imagenes/gastos.png", width=110)

with col8:
    total_gastos = float(obtener_saldo_total("Gastos"))
    var_gastos = float(obtener_variación_hasta_ayer("Gastos",total_gastos))

    st.metric(label="GASTOS TOTALES", value=total_gastos, delta=f"{var_gastos:.2f}%", help = None)


# Simulando lo que viene de SQL (para ver como queda)
data = {
    "Mes": ["2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01", "2025-02", "2025-03", "2025-04"],
    "Activos Totales": [50000, 55000, 60000, 61000, 70000, 90000, 120000, 130000, 125000, 140000],
    "Pasivos Totales": [30000, 31000, 25000, 35000, 45000, 48000, 50000, 55000, 52000, 60000]
}

df = pd.DataFrame(data)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["Mes"],
    y=df["Activos Totales"],
    name="Activos Totales",
    marker_color="#3b82f6"  # azul
))

fig.add_trace(go.Bar(
    x=df["Mes"],
    y=df["Pasivos Totales"],
    name="Pasivos Totales",
    marker_color="#22d3ee"  # celeste
))

# Estilo de layout
fig.update_layout(
    title="Balance General",
    xaxis_title="Mes",
    yaxis_title="Monto (S/.)",
    barmode='group',
    template="simple_white",
    legend=dict(x=0.8, y=1.3),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

#Para correr la aplicación poner en el terminal: streamlit run app.py