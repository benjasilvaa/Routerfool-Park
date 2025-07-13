from parque import Parque

if __name__ == "__main__":
    parque = Parque()

    print("Creando visitantes automáticos (sin mostrar)...")
    parque.crear_visitantes_automaticos(15)

    print("Creando visitantes manuales (se mostrarán movimientos)...")
    parque.crear_visitantes_interactivo()

    print("Simulando parque...")
    parque.simular_parque()
