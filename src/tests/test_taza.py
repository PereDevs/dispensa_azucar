from taza_class import Taza
import time

# Configuración de pines
TRIGGER_PIN = 20  # Pin GPIO conectado al Trigger del sensor de distancia
ECHO_PIN = 21     # Pin GPIO conectado al Echo del sensor de distancia

# Distancia correcta en centímetros para considerar la taza presente
DISTANCIA_CORRECTA = 10

# Crear una instancia de la clase Taza
taza = Taza(TRIGGER_PIN, ECHO_PIN, DISTANCIA_CORRECTA)

try:
    print("[INFO] Iniciando prueba de la taza...")
    while True:
        # Verificar si la taza está presente
        if taza.taza_presente():
            print("[INFO] Taza detectada y en la posición correcta.")
        else:
            print("[INFO] No hay taza o está fuera de posición.")
        
        # Esperar un segundo antes de volver a medir
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Prueba detenida por el usuario.")

finally:
    # Limpieza de recursos
    taza.limpiar()
    print("[INFO] Finalizando prueba.")