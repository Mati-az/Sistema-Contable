import streamlit as st
from services import obtener_saldos_cuentas, obtener
import pandas as pd

st.set_page_config(page_title="Saldos de Cuentas", page_icon="📒", layout="wide")

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
            padding: 2px 5px;
            
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

activos_df = obtener('Activo')
pasivos_df = obtener('Pasivo')
patrimonio_df = obtener('Patrimonio')
ingresos_df = obtener('Ingresos')
gastos_df = obtener('Gastos')

if not activos_df.empty:

    st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
    st.subheader("🟢 Activos")
    cols = st.columns(3)

    for i, row in activos_df.iterrows():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; margin: 10px; background-color: #f9f9f9; width: 400px; height: 160px;">
                    <h3 style="color: #4CAF50; text-align: center;">Cuenta {row['cuenta_id']}</h3>
                    <p><strong>Nombre:</strong> {row['nombre']}</p>
                    <p><strong>Saldo:</strong> S/. {row['saldo']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

if not pasivos_df.empty:
    st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
    st.subheader("🔴 Pasivos")      
    cols = st.columns(3)

    for i, row in pasivos_df.iterrows():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 2px solid #FF5733; border-radius: 10px; padding: 15px; margin: 10px; background-color: #f9f9f9; width: 400px; height: 160px;">
                    <h3 style="color: #FF5733; text-align: center;">Cuenta {row['cuenta_id']}</h3>
                    <p><strong>Nombre:</strong> {row['nombre']}</p>
                    <p><strong>Saldo:</strong> S/. {row['saldo']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

if not patrimonio_df.empty:
    st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
    st.subheader("🟣 Patriminio")
    cols = st.columns(3)

    for i, row in patrimonio_df.iterrows():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 2px solid #9B59B6; border-radius: 10px; padding: 15px; margin: 10px; background-color: #f9f9f9; width: 400px; height: 160px;">
                    <h3 style="color: #9B59B6; text-align: center;">Cuenta {row['cuenta_id']}</h3>
                    <p><strong>Nombre:</strong> {row['nombre']}</p>
                    <p><strong>Saldo:</strong> S/. {row['saldo']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

if not ingresos_df.empty:
    st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
    st.subheader("🟡 Ingresos")
    cols = st.columns(3)

    for i, row in ingresos_df.iterrows():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 2px solid #F1C40F; border-radius: 10px; padding: 15px; margin: 10px; background-color: #f9f9f9; width: 400px; height: 160px;">
                    <h3 style="color: #F1C40F; text-align: center;">Cuenta {row['cuenta_id']}</h3>
                    <p><strong>Nombre:</strong> {row['nombre']}</p>
                    <p><strong>Saldo:</strong> S/. {row['saldo']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

if not gastos_df.empty:
    st.markdown("<hr style='border-top: 2px solid #000000;'>", unsafe_allow_html=True)
    st.subheader("🔵 Gastos")
    cols = st.columns(3)

    for i, row in gastos_df.iterrows():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 2px solid #3498DB; border-radius: 10px; padding: 15px; margin: 10px; background-color: #f9f9f9; width: 400px; height: 160px;">
                    <h3 style="color: #3498DB; text-align: center;">Cuenta {row['cuenta_id']}</h3>
                    <p><strong>Nombre:</strong> {row['nombre']}</p>
                    <p><strong>Saldo:</strong> S/. {row['saldo']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

