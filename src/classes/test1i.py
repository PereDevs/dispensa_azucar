import RPi.GPIO as GPIO
import time

boton_pin = 24  # Cambia este pin si es necesario

GPIO.setmode(GPIO.BCM)
GPIO.setup(boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    # Intentar añadir detección de eventos
    GPIO.add_event_detect(boton_pin, GPIO.FALLING, bouncetime=300)
    print(f"Detección de eventos añadida al pin {boton_pin}")
except RuntimeError as e:
    print(f"[ERROR] {e}")
finally:
    GPIO.cleanup()
