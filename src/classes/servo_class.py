import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # Frecuencia para servos estándar (50 Hz)
        self.pwm.start(0)  # Inicia con duty cycle en 0

    def move(self, angle):
        """
        Mueve el servo a un ángulo específico.
        :param angle: Ángulo de destino (0-180 grados).
        """
        duty_cycle = 2 + (angle / 18)  # Conversión de ángulo a duty cycle
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2)  # Espera mínima para completar el movimiento
        self.pwm.ChangeDutyCycle(0)  # Detiene la señal para evitar zumbidos

    def open_trapdoor(self):
        print("Abriendo trampilla...")
        self.move(90)  # Ángulo de apertura rápida

    def close_trapdoor(self):
        print("Cerrando trampilla...")
        self.move(0)  # Ángulo de cierre rápido

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()