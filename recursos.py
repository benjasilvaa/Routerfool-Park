import threading

class Juego:
    def __init__(self, nombre, capacidad, duracion_segundos):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion_segundos
        self.semaforo = threading.Semaphore(capacidad)

class Bano:
    def __init__(self, nombre, capacidad, duracion_segundos):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion_segundos
        self.semaforo = threading.Semaphore(capacidad)

class Visitante:
    def __init__(self, nombre, mostrar_logs=True):
        self.nombre = nombre
        self.mostrar_logs = mostrar_logs
