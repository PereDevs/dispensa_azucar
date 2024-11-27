import RPi.GPIO as GPIO
import time

boton_pin = 24  # Cambia esto si usas otro pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def boton_callback(channel):
    print("Botón pulsado")

try:
    GPIO.add_event_detect(boton_pin, GPIO.FALLING, callback=boton_callback, bouncetime=300)
    print("Esperando eventos. Presiona Ctrl+C para salir.")
    while True:
        time.sleep(1)  # Mantén el programa corriendo
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
finally:
    GPIO.cleanup()
