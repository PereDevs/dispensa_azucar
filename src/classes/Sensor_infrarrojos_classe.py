import RPi.GPIO as GPIO
import time

class SensorInfrarrojo:
    def __init__(self, pin_sensor):
        """
        Inicializa el sensor infrarrojo.
        
        :param pin_sensor: Pin GPIO conectado al sensor.
        """
        self.pin_sensor = pin_sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_sensor, GPIO.IN)

    def objeto_detectado(self):
        """
        Verifica si el sensor detecta un objeto.
        
        :return: True si el objeto está presente, False si no.
        """
        return GPIO.input(self.pin_sensor) == GPIO.LOW  # Asume que LOW indica objeto presente

    def limpiar(self):
        """
        Limpia los recursos del GPIO.
        """
        GPIO.cleanup()