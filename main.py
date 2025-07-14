from parque import Parque

if __name__ == "__main__":
    parque = Parque()

    print("\n🚨 Creando visitantes automáticos (no se muestran)...")
    parque.crear_visitantes_automaticos(10)

    print("\n🧍 Ingresá visitantes manuales (se verán sus movimientos)...")
    parque.crear_visitantes_interactivo()

    print("\n🎢 Iniciando simulación del parque...\n")
    parque.simular_parque()
