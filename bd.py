import mysql.connector

# Conectarse a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # Cambialo si usás otro usuario
    password="",           # Agregá contraseña si tu MySQL la tiene
    database="routerfool"  # Asegurate de que la base ya existe
)

cursor = conn.cursor()

# Datos de recursos
juegos = [
    ("Montaña Rusa", "Juego", 3, 3),
    ("Sillas Voladoras", "Juego", 2, 2),
    ("Autos Chocadores", "Juego", 2, 4),
    ("Casa del Terror", "Juego", 1, 5)
]

banos = [
    ("Baño Norte", "Baño", 2, 2),
    ("Baño Sur", "Baño", 1, 3),
    ("Baño Este", "Baño", 1, 4),
    ("Baño Oeste", "Baño", 2, 2)
]

recursos = juegos + banos

# Insertar en tabla recursos
insert_query = """
    INSERT INTO recursos (nombre, tipo, capacidad, duracion_segundos)
    VALUES (%s, %s, %s, %s)
"""
cursor.executemany(insert_query, recursos)

conn.commit()
print("✅ Recursos insertados correctamente.")

# Cerrar conexión
cursor.close()
conn.close()
