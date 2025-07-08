import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='routerfool'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def insertar_visitante(visitante):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        sql = "INSERT INTO visitantes (nombre, edad) VALUES (%s, %s)"
        valores = (visitante.nombre, visitante.edad)
        cursor.execute(sql, valores)
        conexion.commit()
        visitante.id = cursor.lastrowid
        cursor.close()
        conexion.close()

def insertar_log(visitante_id, recurso_tipo, recurso_id):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        if recurso_tipo == "Juego":
            tabla_log = "juegos_log"
            columna_id_recurso = "id_juego"
        elif recurso_tipo == "Bano":
            tabla_log = "banos_log"
            columna_id_recurso = "id_bano"
        else:
            cursor.close()
            conexion.close()
            return

        sql = f"INSERT INTO {tabla_log} (id_visitante, {columna_id_recurso}) VALUES (%s, %s)"
        valores = (visitante_id, recurso_id)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
