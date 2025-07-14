import threading

class Juego:
    def __init__(self, nombre, capacidad, duracion_segundos):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion_segundos
        self.semaforo = threading.Semaphore(capacidad)
        self.cola = []
        self.lock = threading.Lock()

class Bano:
    def __init__(self, nombre, capacidad, duracion_segundos):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion_segundos
        self.semaforo = threading.Semaphore(capacidad)
        self.cola = []
        self.lock = threading.Lock()

class Visitante:
    def __init__(self, nombre, tipo="Adulto", mostrar_logs=True, grupo_id=None):
        self.nombre = nombre
        self.tipo = tipo
        self.mostrar_logs = mostrar_logs
        self.grupo_id = grupo_id
