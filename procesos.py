import time
from parque import Parque, Visitante
import threading

def correr_simulacion_con_visitantes(visitantes_serializados, cantidad_automaticos, cola_logs=None, cola_estado=None):
    parque = Parque()

    # Reconstruir visitantes manuales
    for v in visitantes_serializados:
        visitante = Visitante(
            nombre=v["nombre"],
            tipo=v["tipo"],
            mostrar_logs=v.get("mostrar_logs", True),
            grupo_id=v.get("grupo_id")
        )
        parque.visitantes.append(visitante)

    # Crear visitantes automáticos
    parque.crear_visitantes_automaticos(cantidad_automaticos)

    # Redefinir imprimir para mandar logs a cola
    def imprimir_log(texto, mostrar=True):
        if mostrar and cola_logs:
            cola_logs.put(texto)

    parque.imprimir = imprimir_log

    # Mandar estado periódicamente
    def enviar_estado_periodicamente():
        while True:
            if cola_estado:
                estado = {}
                for recurso in parque.juegos + parque.banos:
                    if hasattr(recurso, 'cola'):
                        estado[recurso.nombre] = recurso.cola.qsize()
                    else:
                        estado[recurso.nombre] = recurso.cola_espera
                cola_estado.put(estado)
            time.sleep(1)

    estado_thread = threading.Thread(target=enviar_estado_periodicamente, daemon=True)
    estado_thread.start()

    parque.simular_parque()
