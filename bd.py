import mysql.connector
from mysql.connector import Error
from datetime import datetime

class BaseDatos:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'autocommit': True
        }
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            print("Conexión a la base de datos exitosa.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insertar_recurso(self, nombre, tipo, capacidad, duracion):
        sql = """
        INSERT INTO recursos (nombre, tipo, capacidad, duracion) 
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql, (nombre, tipo, capacidad, duracion))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error al insertar recurso: {e}")
            return None

    def insertar_visitante(self, nombre, tipo, grupo_id=None, automatico=0):
        sql = """
        INSERT INTO visitantes (nombre, tipo, grupo_id, automatico) 
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql, (nombre, tipo, grupo_id, automatico))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error al insertar visitante: {e}")
            return None

    def insertar_uso_recurso(self, visitante_id, recurso_id, inicio, fin, espera=0):
        sql = """
        INSERT INTO uso_recurso (visitante_id, recurso_id, inicio, fin, espera) 
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql, (visitante_id, recurso_id, inicio, fin, espera))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error al insertar uso_recurso: {e}")
            return None


if __name__ == "__main__":
    
    bd = BaseDatos(host="localhost", user="root", password="", database="routerfool")

    id_recurso = bd.insertar_recurso("Montaña Rusa", "Juego", 3, 3)
    print(f"Recurso insertado con id: {id_recurso}")

    id_visitante = bd.insertar_visitante("Juan Perez", "Adulto", None, 0)
    print(f"Visitante insertado con id: {id_visitante}")

    ahora = datetime.now()
    fin = ahora.replace(second=(ahora.second + 5) % 60)  # corregido para no pasarse de 59 segundos

    id_uso = bd.insertar_uso_recurso(id_visitante, id_recurso, ahora, fin, espera=2)
    print(f"Uso recurso insertado con id: {id_uso}")

    bd.cerrar()
