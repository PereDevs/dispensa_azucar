import RPi.GPIO as GPIO
import time

# Configuración del GPIO
BUTTON_PIN = 18   # Cambia este número al pin donde conectaste el botón

GPIO.setmode(GPIO.BCM)  # Usa numeración BCM
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura resistencia pull-up interna

try:
    print("Presiona el botón para probar...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # El botón está presionado
            print("¡Botón presionado!")
            time.sleep(0.2)  # Evita detecciones múltiples rápidas
        else:
            print("Botón no presionado")
            time.sleep(0.2)

except KeyboardInterrupt:
    print("\nPrueba detenida por el usuario.")
finally:
    GPIO.cleanup()  # Limpia la configuración de los pines
