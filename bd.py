import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="routerfool"
)

cursor = conn.cursor()

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

insert_query = """
    INSERT INTO recursos (nombre, tipo, capacidad, duracion_segundos)
    VALUES (%s, %s, %s, %s)
"""
cursor.executemany(insert_query, recursos)

conn.commit()
print("Recursos insertados correctamente.")

cursor.close()
conn.close()
