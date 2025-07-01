import mysql.connector
import threading

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="routerfool"  
)



def insertar_visitantes():
    cursor = conexion.cursor()
    
    nombre = "benjamin "
    edad = 30

    sql = "INSERT INTO visitantes (nombre, edad) VALUES (%s, %s)"
    valores = (nombre, edad)

    cursor.execute(sql, valores)
    conexion.commit()  

    print(f"Se insertó el visitante con id: {cursor.lastrowid}")

    cursor.close()
    conexion.close()
  
visitante = threading.Thread(target=insertar_visitantes)
visitante.start()
visitante.join()

