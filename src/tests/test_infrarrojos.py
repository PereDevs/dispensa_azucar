import RPi.GPIO as GPIO
import time

PIN_SENSOR = 20  # Cambia al pin GPIO correcto

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SENSOR, GPIO.IN)

try:
    while True:
        state = GPIO.input(PIN_SENSOR)
        if state == GPIO.LOW:
            print("Objeto detectado")
        else:
            print("No hay objeto")
        time.sleep(3)  # Intervalo de tiempo
except KeyboardInterrupt:
    print("Finalizando...")
finally:
    GPIO.cleanup()