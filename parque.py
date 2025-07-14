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
        self.grupo_counter = 1
        self.callback_log = None
        self.callback_estado = None

        for recurso in self.juegos + self.banos:
            recurso.cola_espera = 0

    def set_callback_log(self, callback):
        self.callback_log = callback

    def set_callback_estado(self, callback):
        self.callback_estado = callback

    def crear_visitantes_automaticos(self, cantidad):
        for i in range(cantidad):
            nombre = f"AutoVisitante-{i+1}"
            tipo = random.choice(["Niño", "Adulto"])
            visitante = Visitante(nombre, tipo, mostrar_logs=False)
            self.visitantes.append(visitante)

    def crear_visitante_rapido(self):
        nombre = f"Visitante-{len(self.visitantes)+1}"
        visitante = Visitante(nombre, tipo="Adulto", mostrar_logs=True)
        self.visitantes.append(visitante)
        return visitante

    def crear_pack_familiar(self):
        grupo_id = self.grupo_counter
        self.grupo_counter += 1
        base_nombre = f"PackFamiliar-{grupo_id}"
        pack = []
        for i in range(1, 5):
            nombre = f"{base_nombre}-Miembro{i}"
            visitante = Visitante(nombre, tipo="Pack", mostrar_logs=True, grupo_id=grupo_id)
            self.visitantes.append(visitante)
            pack.append(visitante)
        return pack

    def simular_parque(self):
        self.imprimir("Iniciando simulación del parque...", True)

        threads = []
        grupos = {}

        for visitante in self.visitantes:
            if visitante.grupo_id:
                grupos.setdefault(visitante.grupo_id, []).append(visitante)
            else:
                t = threading.Thread(target=self.simular_visita, args=([visitante],))
                t.start()
                threads.append(t)

        for grupo in grupos.values():
            t = threading.Thread(target=self.simular_visita, args=(grupo,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        for recurso in self.juegos + self.banos:
            recurso.cola_espera = 0
        if self.callback_estado:
            self.callback_estado()

    def simular_visita(self, grupo_visitantes):
        nombres = ", ".join(v.nombre for v in grupo_visitantes)
        self.imprimir(f"{nombres} {self.plural(grupo_visitantes, 'llegó', 'llegaron')} al parque.", grupo_visitantes[0].mostrar_logs)
        time.sleep(1)

        juegos_elegidos = random.sample(self.juegos, 2)

        for juego in juegos_elegidos:
            self.usar_recurso(grupo_visitantes, juego)
            time.sleep(1)

        bano = random.choice(self.banos)
        self.usar_recurso(grupo_visitantes, bano)
        time.sleep(1)

        self.imprimir(f"{nombres} {self.plural(grupo_visitantes, 'salió', 'salieron')} del parque.", grupo_visitantes[0].mostrar_logs)

    def usar_recurso(self, grupo, recurso):
        cantidad = len(grupo)
        capacidad = recurso.capacidad
        subgrupos = [grupo[i:i+capacidad] for i in range(0, cantidad, capacidad)]

        for idx, subgrupo in enumerate(subgrupos, 1):
            nombres = ", ".join(v.nombre for v in subgrupo)
            if len(nombres) > 60:
                nombres = nombres[:57] + "..."

            self.imprimir(f"{nombres} {self.plural(subgrupo, 'intenta', 'intentan')} ingresar a {recurso.nombre} (capacidad {capacidad}) [subgrupo {idx}/{len(subgrupos)}]...", subgrupo[0].mostrar_logs)
            time.sleep(0.5)

            esperando = False
            tiempo_espera = 0
            visitantes_en_espera = random.randint(1, 5)

            while True:
                adquiridos = []
                for _ in range(len(subgrupo)):
                    if recurso.semaforo.acquire(blocking=False):
                        adquiridos.append(True)
                    else:
                        break

                if len(adquiridos) == len(subgrupo):
                    recurso.cola_espera = max(0, recurso.cola_espera - len(subgrupo))
                    if self.callback_estado:
                        self.callback_estado()
                    break

                for _ in adquiridos:
                    recurso.semaforo.release()

                if not esperando and tiempo_espera >= 0.5:
                    recurso.cola_espera += len(subgrupo)
                    if self.callback_estado:
                        self.callback_estado()

                    self.imprimir(f"{nombres} {self.plural(subgrupo, 'espera')} para {recurso.nombre} porque no hay espacio suficiente.", subgrupo[0].mostrar_logs)
                    self.imprimir(f"Hay aproximadamente {visitantes_en_espera} personas delante en la cola de {recurso.nombre}.", subgrupo[0].mostrar_logs)
                    esperando = True

                tiempo_espera += 0.5
                time.sleep(0.5)

            self.imprimir(f"{nombres} {self.plural(subgrupo, 'ingresa')} a {recurso.nombre}.", subgrupo[0].mostrar_logs)
            self.imprimir(f"{nombres} {self.plural(subgrupo, 'está usando', 'están usando')} {recurso.nombre} durante {recurso.duracion} segundos.", subgrupo[0].mostrar_logs)
            time.sleep(recurso.duracion)
            self.imprimir(f"{nombres} {self.plural(subgrupo, 'salió', 'salieron')} de {recurso.nombre}.", subgrupo[0].mostrar_logs)

            for _ in range(len(subgrupo)):
                recurso.semaforo.release()
            time.sleep(0.3)

    def imprimir(self, texto, mostrar):
        if mostrar:
            with self.lock_print:
                if self.callback_log:
                    self.callback_log(texto)
                else:
                    print(texto, flush=True)

    def plural(self, grupo, singular, plural=None):
        return singular if len(grupo) == 1 else (plural if plural else singular + "n")
