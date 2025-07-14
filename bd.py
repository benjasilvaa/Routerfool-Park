import mysql.connector

class BaseDatos:
    def __init__(self, host="localhost", user="root", password="", database="routerfool"):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conectar()

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def insertar_recurso(self, nombre, tipo, capacidad, duracion):
        query = '''INSERT INTO recursos (nombre, tipo, capacidad, duracion) 
                   VALUES (%s, %s, %s, %s);'''
        self.cursor.execute(query, (nombre, tipo, capacidad, duracion))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna el id del último recurso insertado

    def insertar_visitante(self, nombre, tipo, grupo_id, automatico):
        query = '''INSERT INTO visitantes (nombre, tipo, grupo_id, automatico) 
                   VALUES (%s, %s, %s, %s);'''
        self.cursor.execute(query, (nombre, tipo, grupo_id, automatico))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna el id del último visitante insertado

    def cerrar(self):
        self.conn.close()
