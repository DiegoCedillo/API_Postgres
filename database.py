import psycopg2
import os
import time

db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

# Lógica de reintento
max_retries = 5
retry_delay = 5

for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(**db_params)
        print("Conexión exitosa.")
        break
    except psycopg2.OperationalError as e:
        print(f"Intento {attempt + 1} fallido: {e}")
        time.sleep(retry_delay)
else:
    raise Exception("No se pudo conectar a la base de datos después de varios intentos")

try:
    # Crear un cursor
    cursor = conn.cursor()

    # Definir la sentencia SQL para crear una tabla
    create_table_query = '''
    CREATE TABLE my_movies (
        ID SERIAL PRIMARY KEY,
        Autor VARCHAR(100),
        Descripcion VARCHAR(100),
        Fecha_Estreno VARCHAR(100)
    );
    '''

    # Ejecutar la sentencia SQL para crear la tabla
    cursor.execute(create_table_query)

    # Confirmar los cambios
    conn.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar el cursor y la conexión
    if conn:
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
