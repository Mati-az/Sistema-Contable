import psycopg2
from psycopg2 import sql

def connect_to_db():
    try:
        # Conexión a la base de datos PostgreSQL
        conn = psycopg2.connect(
            host="localhost",        # Dirección del servidor PostgreSQL
            port="5432",             # Puerto por defecto
            dbname="Sistema Contable", # Nombre de la base de datos
            user="postgres",       # Usuario de la base de datos
            password="1234" # Contraseña
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
