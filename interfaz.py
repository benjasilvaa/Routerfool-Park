import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from parque import Parque
from bd import BaseDatos  # Asegúrate de que bd.py tiene esta clase para MySQL
from recursos import Juego, Bano  # IMPORTA las clases Juego y Bano
from datetime import datetime

class InterfazParque:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación del Parque")
        self.root.geometry("800x600")

        # Conexión a la base de datos MySQL (ajustado para MySQL)
        self.bd = BaseDatos(host="localhost", user="root", password="tu_contraseña", database="routerfool")

        self.parque = Parque()
        self.parque.set_callback_log(self.agregar_log)
        self.parque.set_callback_estado(self.actualizar_estado_colas)

        # Insertar recursos en la BD
        for recurso in self.parque.juegos + self.parque.banos:
            tipo_recurso = "Juego" if isinstance(recurso, Juego) else "Baño"
            recurso.id_bd = self.bd.insertar_recurso(
                recurso.nombre,
                tipo_recurso,  # Tipo calculado dinámicamente
                recurso.capacidad,
                recurso.duracion
            )

        # Configuración de la interfaz
        self.texto_log = ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Consolas", 10))
        self.texto_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.estado_label = tk.Label(root, text="Estado actual de las colas:", justify=tk.LEFT, font=("Consolas", 10))
        self.estado_label.pack(fill=tk.X, padx=10)

        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear Visitante", command=self.crear_visitante).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Crear Pack Familiar", command=self.crear_pack).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Crear Visitantes Automáticos", command=self.crear_automaticos).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Iniciar Simulación", command=self.simular).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Limpiar Logs", command=self.limpiar_logs).pack(side=tk.LEFT, padx=5)

    def agregar_log(self, mensaje):
        self.texto_log.config(state="normal")
        self.texto_log.insert(tk.END, mensaje + "\n")
        self.texto_log.see(tk.END)
        self.texto_log.config(state="disabled")

    def crear_visitante(self):
        visitante = self.parque.crear_visitante_rapido()
        # Insertar en BD
        visitante.id_bd = self.bd.insertar_visitante(
            visitante.nombre,
            visitante.tipo,
            visitante.grupo_id,
            automatico=0
        )
        self.agregar_log(f"Se creó el visitante {visitante.nombre} con ID BD {visitante.id_bd}")

    def crear_pack(self):
        pack = self.parque.crear_pack_familiar()
        for visitante in pack:
            visitante.id_bd = self.bd.insertar_visitante(
                visitante.nombre,
                visitante.tipo,
                visitante.grupo_id,
                automatico=0
            )
        nombres = ", ".join(v.nombre for v in pack)
        self.agregar_log(f"Se creó un pack familiar con: {nombres}")

    def crear_automaticos(self):
        self.parque.crear_visitantes_automaticos(50)
        for visitante in self.parque.visitantes[-50:]:
            visitante.id_bd = self.bd.insertar_visitante(
                visitante.nombre,
                visitante.tipo,
                visitante.grupo_id,
                automatico=1
            )
        self.agregar_log("Se crearon 50 visitantes automáticos.")

    def simular(self):
        threading.Thread(target=self.parque.simular_parque).start()

    def limpiar_logs(self):
        self.texto_log.config(state="normal")
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.config(state="disabled")

    def actualizar_estado_colas(self):
        self.root.after(0, self._actualizar_estado_colas)

    def _actualizar_estado_colas(self):
        texto_estado = "Estado actual de las colas:\n\n"
        for recurso in self.parque.juegos + self.parque.banos:
            cantidad_cola = recurso.cola.qsize() if hasattr(recurso, 'cola') else recurso.cola_espera
            texto_estado += f"{recurso.nombre}: {cantidad_cola} en cola (capacidad: {recurso.capacidad})\n"
        self.estado_label.config(text=texto_estado)

    def cerrar_bd(self):
        self.bd.cerrar()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazParque(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cerrar_bd(), root.destroy()))
    root.mainloop()
