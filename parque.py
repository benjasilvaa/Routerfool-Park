import threading
import random
import time
from recursos import Visitante, Juego, Bano

class Parque:
    def __init__(self):
        self.juegos = [
            Juego("Montaña Rusa", capacidad=3, duracion_segundos=3),
            Juego("Sillas Voladoras", capacidad=2, duracion_segundos=2),
            Juego("Autos Chocadores", capacidad=2, duracion_segundos=4),
            Juego("Casa del Terror", capacidad=1, duracion_segundos=5),
        ]
        self.banos = [
            Bano("Baño Norte", capacidad=2, duracion_segundos=2),
            Bano("Baño Sur", capacidad=1, duracion_segundos=3),
            Bano("Baño Este", capacidad=1, duracion_segundos=4),
            Bano("Baño Oeste", capacidad=2, duracion_segundos=2),
        ]

        self.visitantes = []
        self.lock_print = threading.Lock()

    def crear_visitantes_automaticos(self, cantidad):
        for i in range(cantidad):
            nombre = f"AutoVisitante-{i+1}"
            visitante = Visitante(nombre, mostrar_logs=False)
            self.visitantes.append(visitante)

    def crear_visitantes_interactivo(self):
        try:
            cantidad = int(input("¿Cuántos visitantes deseas crear? "))
        except ValueError:
            print("Cantidad inválida.")
            return

        print("Tipos de visitante disponibles:")
        print("1. Niño")
        print("2. Adulto")
        print("3. Pack Familiar (4 personas)")

        for _ in range(cantidad):
            tipo_opcion = input("Selecciona tipo (1-Niño, 2-Adulto, 3-Pack Familiar): ")

            if tipo_opcion == "1":
                nombre = f"Visitante-{len(self.visitantes)+1}"
                visitante = Visitante(nombre, mostrar_logs=True)
                self.visitantes.append(visitante)
            elif tipo_opcion == "2":
                nombre = f"Visitante-{len(self.visitantes)+1}"
                visitante = Visitante(nombre, mostrar_logs=True)
                self.visitantes.append(visitante)
            elif tipo_opcion == "3":
                # Crear grupo pack familiar (4 visitantes)
                base_nombre = f"PackFamiliar-{len(self.visitantes)//4 + 1}"
                for i in range(1,5):
                    nombre = f"{base_nombre}-Miembro{i}"
                    visitante = Visitante(nombre, mostrar_logs=True)
                    self.visitantes.append(visitante)
                print("Pack Familiar creado con 4 visitantes.")
            else:
                print("Tipo inválido, se crea un adulto por defecto.")
                nombre = f"Visitante-{len(self.visitantes)+1}"
                visitante = Visitante(nombre, mostrar_logs=True)
                self.visitantes.append(visitante)

    def simular_parque(self):
        threads = []
        for visitante in self.visitantes:
            t = threading.Thread(target=self.simular_visita, args=(visitante,))
            t.start()
            threads.append(t)
            time.sleep(0.2)

        for t in threads:
            t.join()

    def simular_visita(self, visitante):
        self.imprimir(f"{visitante.nombre} llegó al parque.", visitante.mostrar_logs)

        juego = random.choice(self.juegos)
        self.usar_recurso(visitante, juego)

        bano = random.choice(self.banos)
        self.usar_recurso(visitante, bano)

        self.imprimir(f"{visitante.nombre} salió del parque.", visitante.mostrar_logs)

    def usar_recurso(self, visitante, recurso):
        self.imprimir(f"{visitante.nombre} intenta ingresar a {recurso.nombre} (capacidad {recurso.capacidad})...", visitante.mostrar_logs)

        esperando = False
        while not recurso.semaforo.acquire(blocking=False):
            if not esperando:
                self.imprimir(f"{visitante.nombre} espera para {recurso.nombre} porque está lleno.", visitante.mostrar_logs)
                esperando = True
            time.sleep(1)

        if esperando:
            self.imprimir(f"{visitante.nombre} dejó de esperar y ahora usa {recurso.nombre}.", visitante.mostrar_logs)
        else:
            self.imprimir(f"{visitante.nombre} pudo entrar directamente a {recurso.nombre}.", visitante.mostrar_logs)

        self.imprimir(f"{visitante.nombre} está usando {recurso.nombre} durante {recurso.duracion} segundos.", visitante.mostrar_logs)
        time.sleep(recurso.duracion)
        self.imprimir(f"{visitante.nombre} terminó de usar {recurso.nombre}.", visitante.mostrar_logs)

        recurso.semaforo.release()

    def imprimir(self, texto, mostrar):
        if mostrar:
            with self.lock_print:
                print(texto)
