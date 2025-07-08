import threading
import queue
import time
from recursos import Visitante  

class Parque:
    def __init__(self):
        self.visitantes = []
        self.cola_juegos = queue.Queue()
        self.cola_banos = queue.Queue()
        self.semaforo_juegos = threading.Semaphore(3)  
        self.semaforo_banos = threading.Semaphore(2)  

    def crear_visitantes_interactivo(self):
        try:
            cantidad = int(input("¿Cuántos visitantes deseas crear? "))
        except ValueError:
            print("Cantidad inválida.")
            return

        print("Tipos de visitante disponibles:")
        print("1. Niño ($1000)")
        print("2. Adulto ($2000)")
        print("3. Pack Familiar ($5000)")

        for i in range(cantidad):
            nombre = f"Visitante-{len(self.visitantes) + 1}"
            tipo_opcion = input(f"Tipo para {nombre} (1-Niño, 2-Adulto, 3-Pack): ")

            if tipo_opcion == "1":
                tipo = "Niño"
                precio = 1000
            elif tipo_opcion == "2":
                tipo = "Adulto"
                precio = 2000
            elif tipo_opcion == "3":
                tipo = "Pack Familiar"
                precio = 5000
            else:
                print("Tipo inválido, se asignará como Adulto por defecto.")
                tipo = "Adulto"
                precio = 2000

            visitante = Visitante(nombre, tipo, precio)
            self.visitantes.append(visitante)
            print(f"{nombre} creado como {tipo} (${precio})")

    def simular_visitantes(self):
        threads = []
        for visitante in self.visitantes:
            t = threading.Thread(target=self.simular_visita, args=(visitante,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def simular_visita(self, visitante):
        print(f"{visitante.nombre} ingresó al parque pagando ${visitante.precio}.")
        time.sleep(1)  
        print(f"{visitante.nombre} salió del parque.")
