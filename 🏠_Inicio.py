import streamlit as st
from services import obtener_saldo_tipo, obtener_variación
import streamlit as st

if "nombre_empresa" not in st.session_state:
    st.session_state.nombre_empresa = "Mi Empresa S.A.C."

st.set_page_config(page_title="Sistema Contable", page_icon="📊", layout="wide")

st.title("📊 Bienvenido al Sistema Contable")

st.markdown("""
**Bienvenido al sistema contable**, una herramienta integral para gestionar y monitorear tus finanzas. 💼

✅ Accede a información detallada sobre tu **Balance General**  
✅ Revisa tu **Estado de Capital Contable**  
✅ Consulta el **Estado de Resultados**  
✅ Realiza **Transacciones** de forma sencilla  
✅ Visualiza los **Saldos de Cuentas**  
✅ Ajusta las **Configuraciones** según tus necesidades

¡Mantén todo tu control financiero en un solo lugar! 📈
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

st.markdown("### 🧮 Resumen Financiero Diario")

st.markdown("""
**Revisa el total de tus activos, pasivos, ingresos y gastos**, junto con su variación porcentual respecto al total hasta el día anterior. 

🔍 Mantente al tanto de las fluctuaciones diarias y toma decisiones informadas para mejorar el control financiero.
            

""")
st.write("")
         
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,1,2,1,2,1,2])

with col1:
    st.image("imagenes/activos.png", width=110)

with col2:
    total_activo = float(obtener_saldo_tipo("Activo"))
    var_activo = float(obtener_variación("Activo",total_activo))
    st.metric(label="ACTIVOS TOTALES", value=total_activo, delta=f"{var_activo:.2f}%", help = None)

with col3:
    st.image("imagenes/pasivos.png", width=110)

with col4:
    total_pasivo = float(obtener_saldo_tipo("Pasivo"))
    var_pasivo = float(obtener_variación("Pasivo",total_pasivo))

    st.metric(label="PASIVOS TOTALES", value=total_pasivo, delta=f"{var_pasivo:.2f}%", help = None)

with col5:
    st.image("imagenes/ingresos.png", width=110)

with col6:
    total_ingresos = float(obtener_saldo_tipo("Ingresos"))
    var_ingresos = float(obtener_variación("Ingresos",total_ingresos))
    st.metric(label="INGRESOS TOTALES", value=total_ingresos, delta=f"{var_ingresos:.2f}%",help=None)

with col7:
    st.image("imagenes/gastos.png", width=110)

with col8:
    total_gastos = float(obtener_saldo_tipo("Gastos"))
    var_gastos = float(obtener_variación("Gastos",total_gastos))
    st.metric(label="GASTOS TOTALES", value=total_gastos, delta=f"{var_gastos:.2f}%", help = None)


#Para correr la aplicación ubicarse en el archivo 🏠_Inicio.py, abrir el terminal y escribir: "streamlit run 🏠_Inicio.py"