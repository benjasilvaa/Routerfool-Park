import multiprocessing
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from parque import Parque
from recursos import Juego, Bano, Visitante
from base_datos import BaseDatos
from procesos import correr_simulacion_con_visitantes

class InterfazParque:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación del Parque")
        self.root.geometry("800x600")

        self.bd = BaseDatos(host="localhost", user="root", password="tu_contraseña", database="routerfool")

        self.parque = Parque()

        for recurso in self.parque.juegos + self.parque.banos:
            tipo = "Juego" if isinstance(recurso, Juego) else "Baño"
            recurso.id_bd = self.bd.insertar_recurso(recurso.nombre, tipo, recurso.capacidad, recurso.duracion)

        self.texto_log = ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Consolas", 10))
        self.texto_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.estado_label = tk.Label(root, text="Estado actual de las colas:", justify=tk.LEFT, font=("Consolas", 10))
        self.estado_label.pack(fill=tk.X, padx=10)

        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear Visitante", command=self.crear_visitante).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Crear Pack Familiar", command=self.crear_pack).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Crear Automáticos", command=self.crear_automaticos).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Simular en Proceso (con Hilos)", command=self.simular_proceso).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Limpiar Logs", command=self.limpiar_logs).pack(side=tk.LEFT, padx=5)

        self.cola_logs = multiprocessing.Queue()
        self.cola_estado = multiprocessing.Queue()

        self.leyendo_logs = True
        threading.Thread(target=self.escuchar_logs, daemon=True).start()
        threading.Thread(target=self.escuchar_estado, daemon=True).start()

    def escuchar_logs(self):
        while self.leyendo_logs:
            try:
                msg = self.cola_logs.get(timeout=0.5)
                self.root.after(0, self.agregar_log, msg)
            except:
                pass

    def escuchar_estado(self):
        while self.leyendo_logs:
            try:
                estado = self.cola_estado.get(timeout=0.5)
                texto = "Estado actual de las colas:\n\n"
                for nombre, cantidad in estado.items():
                    texto += f"{nombre}: {cantidad} en cola\n"
                self.root.after(0, self.estado_label.config, {"text": texto})
            except:
                pass

    def agregar_log(self, mensaje):
        self.texto_log.config(state="normal")
        self.texto_log.insert(tk.END, mensaje + "\n")
        self.texto_log.see(tk.END)
        self.texto_log.config(state="disabled")

    def crear_visitante(self):
        visitante = self.parque.crear_visitante_rapido()
        visitante.id_bd = self.bd.insertar_visitante(visitante.nombre, visitante.tipo, visitante.grupo_id, automatico=0)
        self.agregar_log(f"Se creó el visitante {visitante.nombre} (ID BD: {visitante.id_bd})")

    def crear_pack(self):
        pack = self.parque.crear_pack_familiar()
        for visitante in pack:
            visitante.id_bd = self.bd.insertar_visitante(visitante.nombre, visitante.tipo, visitante.grupo_id, automatico=0)
        nombres = ", ".join(v.nombre for v in pack)
        self.agregar_log(f"Se creó un pack familiar: {nombres}")

    def crear_automaticos(self):
        self.parque.crear_visitantes_automaticos(20)
        for v in self.parque.visitantes[-20:]:
            v.id_bd = self.bd.insertar_visitante(v.nombre, v.tipo, v.grupo_id, automatico=1)
        self.agregar_log("Se crearon 20 visitantes automáticos.")

    def simular_proceso(self):
        # Preparamos lista serializable de visitantes actuales
        visitantes_serializados = []
        for v in self.parque.visitantes:
            visitantes_serializados.append({
                "nombre": v.nombre,
                "tipo": v.tipo,
                "grupo_id": v.grupo_id,
                "mostrar_logs": v.mostrar_logs
            })

        p = multiprocessing.Process(
            target=correr_simulacion_con_visitantes,
            args=(visitantes_serializados, 50, self.cola_logs, self.cola_estado)
        )
        p.start()
        self.agregar_log("Simulación lanzada en proceso con visitantes manuales y automáticos.")

    def limpiar_logs(self):
        self.texto_log.config(state="normal")
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.config(state="disabled")

    def cerrar_bd(self):
        self.leyendo_logs = False
        self.bd.cerrar()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = InterfazParque(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cerrar_bd(), root.destroy()))
    root.mainloop()
