import streamlit as st
from services import obtener_cuentas, transaccion

def main():

    st.set_page_config(page_title="Sistema Contable", page_icon="📊", layout="wide")

    st.title("Bienvenido al Sistema Contable 📊")
    st.write("Selecciona una opción en el menú lateral para continuar.")

    st.markdown("---")

    st.subheader("¿Qué puedes hacer en este sistema?")
    st.write("🔹 Registrar transacciones contables.")  
    st.write("🔹 Generar el balance general.")  
    st.write("🔹 Revisar reportes financieros.")  
    st.write("🔹 Configurar parámetros del sistema.")  

    st.info("Usa el menú lateral para navegar entre las diferentes secciones.")

if __name__ == "__main__":
    main()

#Para correr la aplicación poner en el terminal: streamlit run app.py