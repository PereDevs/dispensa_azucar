import RPi.GPIO as GPIO
import time

# Configuración del GPIO
BUZZER_PIN = 20  # Pin GPIO donde está conectado el buzzer

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Función para reproducir una nota
def play_tone(pin, frequency, duration):
    pwm = GPIO.PWM(pin, frequency)
    pwm.start(50)  # Duty cycle 50%
    time.sleep(duration)
    pwm.stop()

# Melodía del tema principal de Super Mario Bros (más completa y con tempo ajustado)
melody = [
    # Primera sección
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

    # Segunda sección
    (523.25, 0.125),  # Do
    (392.00, 0.125),  # Sol
    (329.63, 0.125),  # Mi
    (440.00, 0.125),  # La
    (493.88, 0.125),  # Si
    (466.16, 0.125),  # La#
    (440.00, 0.125),  # La
    (392.00, 0.125),  # Sol
    (659.25, 0.125),  # Mi
    (784.00, 0.25),   # Sol
    (880.00, 0.25),   # La

    # Tercera sección
    (587.33, 0.125),  # Re
    (784.00, 0.125),  # Sol
    (659.25, 0.125),  # Mi
    (523.25, 0.125),  # Do
    (440.00, 0.125),  # La
    (493.88, 0.125),  # Si
    (523.25, 0.125),  # Do
    (392.00, 0.125),  # Sol
    (659.25, 0.125),  # Mi
    (392.00, 0.25),   # Sol
    (329.63, 0.25),   # Mi

    # Final (repetición simple)
    (659.25, 0.125),  # Mi
    (659.25, 0.125),  # Mi
    (0, 0.125),       # Pausa
    (659.25, 0.125),  # Mi
    (0, 0.125),       # Pausa
    (523.25, 0.125),  # Do
    (659.25, 0.125),  # Mi
    (784.00, 0.25),   # Sol
]

try:
    print("Reproduciendo Super Mario Bros Theme (mejorado). Presiona Ctrl+C para detener.")
    for note in melody:
        frequency, duration = note
        if frequency == 0:
            time.sleep(duration)  # Pausa para silencios
        else:
            play_tone(BUZZER_PIN, frequency, duration)
        time.sleep(0.05)  # Pausa entre notas para mejor fluidez
except KeyboardInterrupt:
    print("\nPrograma detenido")
finally:
    GPIO.cleanup()