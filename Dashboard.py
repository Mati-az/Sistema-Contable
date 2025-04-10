import streamlit as st
from services import obtener_saldototal

def main():

    st.set_page_config(page_title="Sistema Contable", page_icon="📊", layout="wide")

    st.title("Bienvenido al Sistema Contable")

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,1,2,1,2,1,2])
    
    with col1:
        st.image("imagenes/activos.png", width=120)
    with col2:
        saldo_total_activo = float(obtener_saldototal("Activo"))
        st.metric(label="Activos", value=saldo_total_activo, delta=None, help = None)
    with col3:
        st.image("imagenes/pasivos.png", width=100)
    with col4:
        saldo_total_pasivo = float(obtener_saldototal("Pasivo"))
        st.metric(label="Pasivos", value=saldo_total_pasivo, delta=None, help = None)
    with col5:
        st.image("imagenes/ingresos.png", width=100)
    with col6:
        total_ingresos = float(obtener_saldototal("Ingresos"))
        st.metric(label="Ingresos", value=total_ingresos, delta=None,help=None)
    with col7:
        st.image("imagenes/gastos.png", width=100)
    with col8:
        total_gastos = float(obtener_saldototal("Gastos"))
        st.metric(label="Gastos", value=total_gastos, delta=None, help = None)

    st.markdown("---")

    st.subheader("¿Qué puedes hacer en este sistema?")
    st.write("🔹 Registrar transacciones contables.")
    st.write("🔹 Generar el balance general.")
    st.write("🔹 Revisar reportes financieros.")
    st.write("🔹 Configurar parámetros del sistema.")

    st.info("Usa el menú lateral para navegar entre las diferentes secciones.")

    st.sidebar.title("🖥️ Dashboard")

if __name__ == "__main__":
    main()

#Para correr la aplicación poner en el terminal: streamlit run app.py