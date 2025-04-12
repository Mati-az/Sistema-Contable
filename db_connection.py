import psycopg2
import os
from psycopg2 import sql

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",       
            port="5432",            
            dbname="Sistema Contable", # Nombre de la base de datos
            user="postgres",       # Usuario de la base de datos
            password=os.getenv("DB_PASSWORD", "1234") # Contraseña se obtiene de la variable de entorno DB_PASSWORD, por defecto es 1234
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
