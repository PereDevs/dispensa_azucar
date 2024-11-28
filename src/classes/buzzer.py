import RPi.GPIO as GPIO
import time

# Configuración del GPIO
BUZZER_PIN = 20  # Pin GPIO donde está conectado el buzzer

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Función para reproducir una nota con ajustes
def play_tone(pin, frequency, duration):
    pwm = GPIO.PWM(pin, frequency)
    pwm.start(30)  # Cambiar el duty cycle a 30%
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        pass
    for duty_cycle in range(70, 0, -5):  # Gradualmente reducir el duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.01)
    pwm.stop()

# Melodía ajustada
melody = [
    (659.25, 0.125),  # Mi
    (659.25, 0.125),  # Mi
    (0, 0.125),       # Pausa
    (659.25, 0.125),  # Mi
    (0, 0.125),       # Pausa
    (523.25, 0.125),  # Do
    (659.25, 0.125),  # Mi
    (784.00, 0.25),   # Sol
    (0, 0.25),        # Pausa
    (392.00, 0.25),   # Sol
]

# Función para reproducir la melodía completa
def play_melody():
    try:
        for note in melody:
            frequency, duration = note
            if frequency == 0:
                time.sleep(duration)  # Pausa para silencios
            else:
                play_tone(BUZZER_PIN, frequency, duration)
            time.sleep(0.05)  # Pausa entre notas
    except KeyboardInterrupt:
        print("\n[INFO] Melodía interrumpida por el usuario.")
    finally:
        GPIO.cleanup()

