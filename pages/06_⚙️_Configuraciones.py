import streamlit as st

st.set_page_config(page_title="Configuraciones", page_icon="⚙️", layout="wide")

st.title("⚙️ Configuraciones")

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

# Página de configuración
st.title("Configuración de la Empresa")

# Crear un valor por defecto si no existe
if "nombre_empresa" not in st.session_state:
    st.session_state.nombre_empresa = "Mi Empresa S.A.C."

# Input para cambiar el nombre
nuevo_nombre = st.text_input(
    "Nombre de la empresa",
    value=st.session_state.nombre_empresa,
    help="Ingresa el nombre que deseas mostrar en los reportes."
)

# Botón para guardar
if st.button("Guardar cambios"):
    st.session_state.nombre_empresa = nuevo_nombre
    st.success("¡Nombre de empresa actualizado!")

# Mostrar el nombre actual
st.write("**Nombre actual:**", st.session_state.nombre_empresa)