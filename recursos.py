import threading

class Juego:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.semaforo = threading.Semaphore(capacidad)

    def usar(self, visitante):
        print(f"{visitante.id} intenta ingresar al juego {self.nombre}")
        with self.semaforo:
            print(f"{visitante.id} está usando el juego {self.nombre}")
            # Aquí podés poner el tiempo que dura usar el juego
            # Ejemplo: time.sleep(random.uniform(1, 3))
        print(f"{visitante.id} salió del juego {self.nombre}")

class Bano:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.semaforo = threading.Semaphore(capacidad)

    def usar(self, visitante):
        print(f"{visitante.id} intenta ingresar al baño {self.nombre}")
        with self.semaforo:
            print(f"{visitante.id} está usando el baño {self.nombre}")
            # Aquí podés poner el tiempo que dura usar el baño
            # Ejemplo: time.sleep(random.uniform(1, 2))
        print(f"{visitante.id} salió del baño {self.nombre}")

class Visitante:
    def __init__(self, id, tipo, precio):
        self.id = id
        self.tipo = tipo
        self.precio = precio
