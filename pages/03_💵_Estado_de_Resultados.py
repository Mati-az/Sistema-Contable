import streamlit as st
from services import calcular_estado_resultados
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # o 'Spanish_Spain.1252' en Windows
info_fecha = datetime.now().strftime("Mes terminado el %d de %B del %Y")

st.set_page_config(page_title="Estado de Resultados", page_icon="💵", layout="wide")

st.title("💵 Estado de Resultados")


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



resultados = calcular_estado_resultados()

if resultados:
    st.markdown(f"### {st.session_state.nombre_empresa}")
    st.subheader(f"Mes terminado el {info_fecha}")
    st.write("---")

    # Ingresos
    st.markdown("**Ingresos:**")
    for nombre, saldo in resultados["ingresos"]:
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{nombre}", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right;'>S/ {saldo:,.2f}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"**Ingresos Totales**", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right; font-weight: bold;'>S/ {resultados['total_ingresos']:,.2f}</div>", unsafe_allow_html=True)

    st.write("---")

    # Gastos
    st.markdown("**Gastos:**")
    for nombre, saldo in resultados["gastos"]:
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{nombre}", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right;'>S/ {saldo:,.2f}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"**Gastos Totales**", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right; font-weight: bold;'>S/ {resultados['total_gastos']:,.2f}</div>", unsafe_allow_html=True)

    st.write("")

    utilidad_neta = resultados["utilidad_neta"]
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"**Utilidad Neta**", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right; font-weight: bold;'>S/ {utilidad_neta:,.2f}</div>", unsafe_allow_html=True)
