import RPi.GPIO as GPIO
import time

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Iniciar PWM
pwm = GPIO.PWM(18, 50)  # 50 Hz es la frecuencia típica para servos
pwm.start(0)  # Inicia con un duty cycle de 0%

try:
    while True:
        # Mover a 0 grados
        pwm.ChangeDutyCycle(2.5)  # 2.5% ciclo para 0 grados
        time.sleep(1)
        
        # Mover a 90 grados
        pwm.ChangeDutyCycle(7.5)  # 7.5% ciclo para 90 grados
        time.sleep(1)
        
        # Mover a 180 grados
        pwm.ChangeDutyCycle(12.5)  # 12.5% ciclo para 180 grados
        time.sleep(1)
        
finally:
    pwm.stop()
    GPIO.cleanup()
