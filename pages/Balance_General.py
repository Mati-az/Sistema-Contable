import streamlit as st
import pandas as pd
from services import get_balance_general, get_db_version

# Título del reporte
st.title("📊 Estado de Situación Financiera")

# Primero obtén un pequeño valor que cambie cuando cambia la base de datos
db_version = get_db_version()

# Obtener datos
df = get_balance_general(db_version)

if df is None or df.empty:
    st.warning("⚠ No hay cuentas con saldo distinto de 0.")
else:
    # Separar por categorías
    activos_corrientes = df[df["categoria"] == "Activo Corriente"]
    activos_no_corrientes = df[df["categoria"] == "Activo No Corriente"]
    pasivos_corrientes = df[df["categoria"] == "Pasivo Corriente"]
    pasivos_no_corrientes = df[df["categoria"] == "Pasivo No Corriente"]
    patrimonio = df[df["categoria"] == "Patrimonio"]

    # Calcular totales
    total_activo_corr = activos_corrientes["saldo"].sum()
    total_activo_no_corr = activos_no_corrientes["saldo"].sum()
    total_pasivo_corr = pasivos_corrientes["saldo"].sum()
    total_pasivo_no_corr = pasivos_no_corrientes["saldo"].sum()
    total_pasivo = total_pasivo_corr + total_pasivo_no_corr  # Total Pasivo
    total_patrimonio = patrimonio["saldo"].sum()
    activo_total = total_activo_corr + total_activo_no_corr
    pasivo_patrimonio_total = total_pasivo_corr + total_pasivo_no_corr + total_patrimonio

    # Crear layout con 2 columnas
    col1, col2 = st.columns(2)

    # 📌 SECCIÓN ACTIVO
    with col1:
        st.subheader("🟢 ACTIVO")
        
        # Activo Corriente
        if not activos_corrientes.empty:
            st.markdown("### Activo Corriente")
            st.table(activos_corrientes[["nombre", "saldo"]].set_index("nombre"))
            st.markdown(f"**Total Activo Corriente: {total_activo_corr:,.2f}**")

        # Activo No Corriente
        if not activos_no_corrientes.empty:
            st.markdown("### Activo No Corriente")
            st.table(activos_no_corrientes[["nombre", "saldo"]].set_index("nombre"))
            st.markdown(f"**Total Activo No Corriente: {total_activo_no_corr:,.2f}**")

        st.markdown(f"### 🟡 **ACTIVO TOTAL: {activo_total:,.2f}**")

    # 📌 SECCIÓN PASIVO Y PATRIMONIO
    with col2:
        st.subheader("🔴 PASIVO")

        # Pasivo Corriente
        if not pasivos_corrientes.empty:
            st.markdown("### Pasivo Corriente")
            st.table(pasivos_corrientes[["nombre", "saldo"]].set_index("nombre"))
            st.markdown(f"**Total Pasivo Corriente: {total_pasivo_corr:,.2f}**")

        # Pasivo No Corriente
        if not pasivos_no_corrientes.empty:
            st.markdown("### Pasivo No Corriente")
            st.table(pasivos_no_corrientes[["nombre", "saldo"]].set_index("nombre"))
            st.markdown(f"**Total Pasivo No Corriente: {total_pasivo_no_corr:,.2f}**")

        # 📌 Mostrar Total Pasivo antes del Patrimonio
        st.markdown(f"### 🟠 **TOTAL PASIVO: {total_pasivo:,.2f}**")

        # Patrimonio
        st.subheader("🟣 PATRIMONIO")
        st.table(patrimonio[["nombre", "saldo"]].set_index("nombre"))
        st.markdown(f"**Total Patrimonio: {total_patrimonio:,.2f}**")

        st.markdown(f"### 🟡 **TOTAL PASIVO + PATRIMONIO: {pasivo_patrimonio_total:,.2f}**")

    # 📌 Verificación de Balance
    if activo_total == pasivo_patrimonio_total:
        st.success("✅ El Balance General está cuadrado.")
    else:
        st.error("❌ El Balance General no cuadra. Verificar los datos.")
