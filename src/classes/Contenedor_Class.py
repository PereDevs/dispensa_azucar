import RPi.GPIO as GPIO
import time
import mysql.connector
from mysql.connector import Error
from classes.LCD_IC2_classe import LCD_I2C

GPIO.setwarnings(False)

class Contenedor:
    def __init__(self, capacidad_total, motor_pin, boton_pin, lcd, tipo_azucar, db_config):
        self.capacidad_total = capacidad_total
        self.motor_pin = motor_pin
        self.boton_pin = boton_pin
        self.lcd = lcd
        self.tipo_azucar = tipo_azucar  # Tipo de azúcar (1: Blanco, 2: Moreno, 3: Edulcorante)
        self.db_config = db_config  # Configuración de la base de datos
        self.cantidad_actual = self.obtener_cantidad_actual()  # Cantidad disponible desde la base de datos
        self.estado = "lleno" if self.cantidad_actual > 0 else "vacio"

        # Configuración del hardware
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.servo = GPIO.PWM(self.motor_pin, 50)
        self.servo.start(0)

    def obtener_cantidad_actual(self):
        """
        Consulta la cantidad disponible y el estado del contenedor desde la base de datos.
        """
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                SELECT cantidad_disponible, estado, capacidad_total
                FROM contenedores
                WHERE id_azucar = %s
            """
            cursor.execute(query, (self.tipo_azucar,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                cantidad_disponible, estado, capacidad_total = resultado
                self.estado = estado
                self.capacidad_total = capacidad_total
                return cantidad_disponible
            else:
                print("[ERROR] Contenedor no encontrado en la base de datos.")
                return 0
        except Error as e:
            print(f"[ERROR] Al consultar la base de datos: {e}")
            return 0

    def dispensar_azucar(self, cantidad):
        """
        Dispensar una cantidad específica de azúcar.
        """
        self.cantidad_actual = self.obtener_cantidad_actual()  # Actualizar la cantidad actual

        if self.cantidad_actual <= 0 or self.estado == "vacio":
            self.estado = "vacio"
            self.lcd.clear()
            self.lcd.write("Azúcar vacío", line=1)
            self.lcd.write("Pulsar boton", line=2)
            return "Error: Contenedor vacío"

        if cantidad > self.cantidad_actual:
            self.lcd.clear()
            self.lcd.write("No hay suficiente", line=1)
            self.lcd.write(f"Azúcar. Disp: {self.cantidad_actual}g", line=2)
            time.sleep(3)
            return "Error: No hay suficiente azúcar disponible"

        # Abrir el dispensador
        self.controlar_motor(90)
        self.lcd.clear()
        self.lcd.write(f"Sirviendo {cantidad}g", line=1)
        time.sleep(cantidad * 0.5)  # Simular tiempo de dispensado
        self.controlar_motor(0)  # Cerrar el dispensador

        # Registrar el consumo
        self.registrar_dispenso(cantidad)
        self.cantidad_actual -= cantidad  # Actualizar localmente
        self.actualizar_estado()
        return f"Dispensado: {cantidad} g"

    def registrar_dispenso(self, cantidad):
        """
        Actualiza la base de datos al dispensar azúcar.
        """
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                UPDATE contenedores
                SET cantidad_disponible = cantidad_disponible - %s,
                    estado = CASE
                        WHEN cantidad_disponible - %s <= 0 THEN 'vacio'
                        WHEN cantidad_disponible - %s < capacidad_total THEN 'parcial'
                        ELSE 'lleno'
                    END
                WHERE id_azucar = %s
            """
            cursor.execute(query, (cantidad, cantidad, cantidad, self.tipo_azucar))
            conexion.commit()
            conexion.close()
        except Error as e:
            print(f"[ERROR] Al actualizar el estado del contenedor: {e}")

    def rellenar_contenedor(self):
        """
        Actualiza la cantidad disponible al rellenar el contenedor.
        """
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                UPDATE contenedores
                SET cantidad_disponible = capacidad_total,
                    estado = 'lleno'
                WHERE id_azucar = %s
            """
            cursor.execute(query, (self.tipo_azucar,))
            conexion.commit()
            conexion.close()

            self.cantidad_actual = self.capacidad_total
            self.estado = "lleno"

            self.lcd.clear()
            self.lcd.write("Contenedor lleno", line=1)
            time.sleep(3)
        except Error as e:
            print(f"[ERROR] Al rellenar el contenedor: {e}")

    def actualizar_estado(self):
        """
        Actualiza el estado del contenedor basado en la cantidad actual.
        """
        if self.cantidad_actual <= 0:
            self.estado = "vacio"
            self.lcd.write("Azúcar vacío", line=1)
        elif self.cantidad_actual < self.capacidad_total:
            self.estado = "parcial"
        else:
            self.estado = "lleno"


    def controlar_motor(self, angulo):
        """
        Controla el motor moviéndolo al ángulo deseado.
        Asegura que el motor comience desde la posición 0 antes de realizar el movimiento.
        """
        try:
            # Mover el motor a la posición inicial (0 grados)
            self.servo.ChangeDutyCycle(7.5)  # Duty cycle para 0 grados
            time.sleep(0.5)  # Tiempo para asegurar la posición inicial

            # Calcular el ciclo de trabajo para el ángulo deseado
            duty_cycle = 2 + (angulo / 18)  # Convertir ángulo a ciclo de trabajo
            self.servo.ChangeDutyCycle(duty_cycle)
            time.sleep(2)  # Tiempo para completar el movimiento

            # Detener el motor
            self.servo.ChangeDutyCycle(7.5)  # Duty cycle para 0 grado
            time.sleep(0.5)  # Tiempo para asegurar la posición inicial
            self.servo.ChangeDutyCycle(0)
        except Exception as e:
            print(f"[ERROR] No se pudo controlar el motor: {e}")
