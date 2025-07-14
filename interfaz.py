import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from parque import Parque

class InterfazParque:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación del Parque")
        self.root.geometry("800x600")

        self.parque = Parque()
        self.parque.set_callback_log(self.agregar_log)
        self.parque.set_callback_estado(self.actualizar_estado_colas)

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
        self.agregar_log(f"Se creó el visitante {visitante.nombre}")

    def crear_pack(self):
        pack = self.parque.crear_pack_familiar()
        nombres = ", ".join(v.nombre for v in pack)
        self.agregar_log(f"Se creó un pack familiar con: {nombres}")

    def crear_automaticos(self):
        self.parque.crear_visitantes_automaticos(50)
        self.agregar_log("Se crearon 20 visitantes automáticos.")

    def simular(self):
        threading.Thread(target=self.parque.simular_parque).start()

    def limpiar_logs(self):
        self.texto_log.config(state="normal")
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.config(state="disabled")

    def actualizar_estado_colas(self):
        texto_estado = "Estado actual de las colas:\n\n"
        for recurso in self.parque.juegos + self.parque.banos:
            texto_estado += f"{recurso.nombre}: {recurso.cola_espera} en cola (capacidad: {recurso.capacidad})\n"
        self.estado_label.config(text=texto_estado)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazParque(root)
    root.mainloop()
