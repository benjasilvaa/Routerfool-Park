import mysql.connector
from mysql.connector import Error

class BaseDatos:
    def __init__(self, host="localhost", user="root", password="", database="routerfool"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conectar()

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password'  # por si usas MySQL 8+
            )
            self.cursor = self.conn.cursor()
            print("Conexión exitosa a la base de datos MySQL.")
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def insertar_recurso(self, nombre, tipo, capacidad, duracion):
        query = '''INSERT INTO recursos (nombre, tipo, capacidad, duracion) 
                   VALUES (%s, %s, %s, %s);'''
        self.cursor.execute(query, (nombre, tipo, capacidad, duracion))
        self.conn.commit()
        return self.cursor.lastrowid

    def insertar_visitante(self, nombre, tipo, grupo_id, automatico):
        query = '''INSERT INTO visitantes (nombre, tipo, grupo_id, automatico) 
                   VALUES (%s, %s, %s, %s);'''
        self.cursor.execute(query, (nombre, tipo, grupo_id, automatico))
        self.conn.commit()
        return self.cursor.lastrowid

    def cerrar(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexión MySQL cerrada.")
