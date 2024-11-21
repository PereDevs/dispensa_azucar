import RPi.GPIO as GPIO
import time

class SensorDistancia:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeració de pins
        GPIO.setup(self.trigger_pin, GPIO.OUT)  # Configura el pin trigger com a sortida
        GPIO.setup(self.echo_pin, GPIO.IN)  # Configura el pin echo com a entrada

    def mesura_distancia(self):
        """Mesura la distància en centímetres (sincrònic)."""
        # Envia un pols de 10 µs pel pin trigger per iniciar la mesura
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)  # Pols de 10 microsegons
        GPIO.output(self.trigger_pin, GPIO.LOW)

        # Mesura el temps que tarda el senyal d’echo en tornar
        start_time = time.time()
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        # Calcula el temps de vol del pols
        elapsed_time = stop_time - start_time
        # Calcula la distància (en centímetres)
        distancia = (elapsed_time * 34300) / 2  # velocitat del so en cm/s
        return distancia

    def activar_interrupcio(self, callback):
        """Configura una interrupció per al pin echo."""
        GPIO.add_event_detect(self.echo_pin, GPIO.RISING, callback=callback)

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()
