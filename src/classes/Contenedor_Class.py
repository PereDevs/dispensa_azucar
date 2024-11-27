import RPi.GPIO as GPIO
import time
from classes.LCD_IC2_classe import LCD_I2C
import threading  # Para manejar la consulta manual en un hilo separado

GPIO.setwarnings(False)

class Contenedor:
    def __init__(self, capacidad_total, motor_pin, boton_pin, lcd):
        self.capacidad_total = capacidad_total  # Capacidad total del contenedor
        self.cantidad_actual = capacidad_total  # Inicialmente está lleno
        self.motor_pin = motor_pin  # Pin del servomotor
        self.boton_pin = boton_pin  # Pin del botón
        self.lcd = lcd  # Pantalla LCD para mensajes
        self.estado = "lleno"  # Estado inicial del contenedor

        # Configuración de los pines
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Botón con pull-up interno
        
        # PWM para el servomotor
        self.servo = GPIO.PWM(self.motor_pin, 50)  # Frecuencia de 50Hz
        self.servo.start(0)  # Inicializar el servo en la posición 0°

        # Iniciar detección de presión prolongada en un hilo separado
        self.hilo_deteccion = threading.Thread(target=self.detectar_presion_prolongada, daemon=True)
        self.hilo_deteccion.start()

    def detectar_presion_prolongada(self):
        """
        Detecta si el botón se mantiene presionado durante 5 segundos para confirmar el llenado del contenedor.
        """
        tiempo_inicio = None

        while True:
            if GPIO.input(self.boton_pin) == GPIO.LOW:  # Botón presionado
                if tiempo_inicio is None:
                    tiempo_inicio = time.time()  # Registrar el tiempo en que se presionó el botón

                # Calcular la duración de la presión
                duracion_presion = time.time() - tiempo_inicio
                if duracion_presion >= 5:  # Si la presión dura 5 segundos o más
                    print("[INFO] Botón mantenido durante 5 segundos. Confirmando llenado.")
                    self.confirmar_llenado()
                    tiempo_inicio = None  # Resetear el tiempo para futuras detecciones
            else:
                tiempo_inicio = None  # Resetear si se suelta el botón antes de los 5 segundos

            time.sleep(0.1)  # Reducir la carga de la CPU

    def confirmar_llenado(self):
        """
        Confirma que el contenedor ha sido llenado.
        """
        self.cantidad_actual = self.capacidad_total
        self.estado = "lleno"
        self.lcd.clear()
        self.lcd.write("Contenedor lleno", line=1)
        print("[INFO] Contenedor lleno confirmado.")

    def controlar_motor(self, angulo):
        """
        Controla el servomotor moviéndolo al ángulo especificado.
        :param angulo: Ángulo al que mover el servomotor (0° a 180°).
        """
        duty_cycle = 2 + (angulo / 18)  # Conversión de ángulo a ciclo de trabajo
        self.servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Esperar a que el servo complete el movimiento
        self.servo.ChangeDutyCycle(0)  # Apagar el servo para evitar sobrecalentamiento

    def dispensar_azucar(self, cantidad):
        """
        Dispensar una cantidad específica de azúcar.
        :param cantidad: Cantidad de azúcar en gramos.
        """
        if self.cantidad_actual <= 0:
            self.estado = "vacio"
            self.lcd.write("Azúcar vacío", line=1)
            return "Error: Contenedor vacío"

        if cantidad > self.cantidad_actual:
            cantidad = self.cantidad_actual  # No se puede dispensar más de lo que queda

        # Abrir el dispensador
        self.controlar_motor(90)
        self.lcd.write(f"Sirviendo {cantidad}g", line=1)
        time.sleep(cantidad * 0.5)  # Simular tiempo de dispensado

        # Cerrar el dispensador
        self.controlar_motor(0)

        self.cantidad_actual -= cantidad  # Restar la cantidad dispensada
        self.actualizar_estado()
        return f"Dispensado: {cantidad} g"

    def actualizar_estado(self):
        if self.cantidad_actual <= 0:
            self.estado = "vacio"
            self.lcd.write("Azúcar vacío", line=1)
        else:
            self.estado = "lleno"
            self.lcd.write("Contenedor listo", line=1)
