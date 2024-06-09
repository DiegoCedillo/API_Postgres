import os
import time
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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


class Movie(BaseModel):
    table_name: str
    Autor: str
    Descripcion: str
    Fecha_Estreno: str

class Edit(BaseModel):
    table_name: str
    id: int
    col: str
    edit: str

class Delete(BaseModel):
    table_name: str
    id: int


@app.get('/movie')
def get_movie():

    temporal_list = []

    with conn.cursor() as cursor:
        
        try:
            get_data_query = '''
            SELECT * FROM my_movies
            '''
            
            cursor.execute(get_data_query)

            rows = cursor.fetchall()

            for row in rows:
                print(row)
                temporal_list.append(row)
        except:
            print("Error con la consulta GET")

    return {"message": temporal_list}


@app.post('/movie')
def insert_movie(task:Movie):

    with conn.cursor() as cursor:
        
        try:
            insert_data_query = f'''
            INSERT INTO {task.table_name} (Autor, Descripcion, Fecha_Estreno) VALUES (%s, %s, %s);
            '''

            data_to_insert = (task.Autor, task.Descripcion, task.Fecha_Estreno)
            cursor.execute(insert_data_query,data_to_insert )
            conn.commit()

        except Exception as e:
            print(e)
            print("Error con la consulta POST")

    return {"message": "Creado correctamente"}


@app.put('/movie/')
def edit_movie(task: Edit):
    with conn.cursor() as cursor:
        
        try:
            edit_data_query = f'''
            UPDATE {task.table_name} SET {task.col} = '{task.edit}' WHERE id = {task.id};
            '''

            cursor.execute(edit_data_query)
            conn.commit()

        except Exception as e:
            print(e)
            print("Error con la consulta POST")

    return {"message": "Modificado correctamente"}


@app.delete('/movie/')
def delete_movie(task: Delete):
    with conn.cursor() as cursor:
        
        try:
            delete_data_query = f'''
            DELETE FROM {task.table_name} WHERE id = {task.id};
            '''

            #data_to_insert = (task.Autor, task.Descripcion, task.Fecha_Estreno)
            cursor.execute(delete_data_query)
            conn.commit()

        except Exception as e:
            print(e)
            print("Error con la consulta POST")

    return {"message": "Eliminado correctamente"}

