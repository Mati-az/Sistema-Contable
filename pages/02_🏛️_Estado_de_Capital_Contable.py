import streamlit as st
import pandas as pd
#from services import calcular_estado
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Estado de Resultados", page_icon="🏛️", layout="wide")

st.title("🏛️ Estado de Capital Contable")

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


# Obtener fechas automáticamente
hoy = date.today()
primer_dia_mes_actual = hoy.replace(day=1)
ultimo_dia_mes_anterior = primer_dia_mes_actual - relativedelta(days=1)
primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

# Fechas completas con horas
fecha_fin = datetime.combine(hoy, datetime.max.time())
fecha_inicio = datetime.combine(primer_dia_mes_actual, datetime.min.time())
fecha_ultimo_mes = datetime.combine(ultimo_dia_mes_anterior, datetime.max.time())


# Llamada a la función y asignación del diccionario a una variable
# resultados = calcular_estado_capital()

# Asignación de valores del diccionario a variables separadas
#capital_inicial = resultados['capital_inicial']
#inversiones = resultados['inversiones']
#retiros = resultados['retiros']
#ingresos = resultados['ingresos']
#gastos = resultados['gastos']
#utilidad_neta = resultados['utilidad_neta']
#capital_final = resultados['capital_final']

# Mostrar en Streamlit
st.markdown("""
<style>
.box {
    border: 2px solid #ccc;
    border-radius: 15px;
    padding: 20px;
    background-color: #f9f9f9;
}
table {
    width: 100%;
    border-collapse: collapse;
}
td {
    padding: 8px;
}
tr.total {
    border-top: 2px solid #000;
    font-weight: bold;
}
.right {
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

mes = fecha_fin.strftime("%B").capitalize()
anio = fecha_fin.strftime("%Y")
st.subheader(f"Mes terminado el {fecha_fin.strftime('%d de %B de %Y')}")

st.write(f"**Capital, 1 de {mes} de {anio}:** ${capital_inicial:,.2f}")
st.write(f"**Más: Inversiones realizadas por el propietario:** ${inversiones:,.2f}")
st.write(f"**Utilidad neta para el mes:** ${utilidad_neta:,.2f}")
st.write(f"**Menos: Retiros del propietario:** ${retiros:,.2f}")
st.markdown("---")
st.write(f"**Capital, {fecha_fin.strftime('%d de %B de %Y')}:** ${capital_final:,.2f}")
