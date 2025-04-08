import streamlit as st
from services import calcular_estado_resultados

resultados = calcular_estado_resultados()

if resultados:
    st.markdown("### SMART TOUCH LEARNING")
    st.markdown("#### Estado de resultados")
    st.markdown("##### Mes terminado el 30 de abril de 2010")
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
