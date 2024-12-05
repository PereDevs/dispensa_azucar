import time
import mysql.connector
from gpiozero import Button

class EntradaDatosCompletos:
    def __init__(self, pin_adelante, pin_atras, pin_confirmar, lcd, db_config):
        """
        Clase para manejar el flujo completo de entrada de nombre, cantidad, tipo y confirmación.
        """
        self.boton_adelante = Button(pin_adelante, pull_up=True)
        self.boton_atras = Button(pin_atras, pull_up=True)
        self.boton_confirmar = Button(pin_confirmar, pull_up=True, hold_time=3)
        self.lcd = lcd
        self.db_config = db_config

        # Estados del flujo
        self.modo_actual = "nombre"  # Puede ser "nombre", "cantidad", "tipo", o "confirmar"
        self.finalizado = False

        # Datos introducidos
        self.nombre = ""
        self.cantidad = ""
        self.tipos_azucar = ["Blanco", "Moreno", "Edulcorante"]
        self.tipo_actual = 0
        self.confirmacion = 0  # 0 = No, 1 = Sí
        self.indice_letra = 0
        self.indice_numero = 0

        # Alfabetos y dígitos
        self.alfabeto = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.numeros = "0123456789"

        # Configurar eventos de los botones
        self.boton_adelante.when_pressed = self.mover_adelante
        self.boton_atras.when_pressed = self.mover_atras
        self.boton_confirmar.when_pressed = self.confirmar_opcion
        self.boton_confirmar.when_held = self.procesar_finalizacion

        # Mostrar estado inicial
        self.mostrar_estado()

    def mover_adelante(self):
        """Cambia al siguiente valor dependiendo del modo."""
        if self.modo_actual == "nombre":
            self.indice_letra = (self.indice_letra + 1) % len(self.alfabeto)
        elif self.modo_actual == "cantidad":
            self.indice_numero = (self.indice_numero + 1) % len(self.numeros)
        elif self.modo_actual == "tipo":
            self.tipo_actual = (self.tipo_actual + 1) % len(self.tipos_azucar)
        elif self.modo_actual == "confirmar":
            self.confirmacion = (self.confirmacion + 1) % 2  # Alterna entre 0 (No) y 1 (Sí)
        self.mostrar_estado()

    def mover_atras(self):
        """Cambia al valor anterior dependiendo del modo."""
        if self.modo_actual == "nombre":
            self.indice_letra = (self.indice_letra - 1) % len(self.alfabeto)
        elif self.modo_actual == "cantidad":
            self.indice_numero = (self.indice_numero - 1) % len(self.numeros)
        elif self.modo_actual == "tipo":
            self.tipo_actual = (self.tipo_actual - 1) % len(self.tipos_azucar)
        elif self.modo_actual == "confirmar":
            self.confirmacion = (self.confirmacion - 1) % 2  # Alterna entre 0 (No) y 1 (Sí)
        self.mostrar_estado()

    def confirmar_opcion(self):
        """Confirma la selección actual y avanza en el flujo si corresponde."""
        if self.modo_actual == "nombre":
            letra = self.alfabeto[self.indice_letra]
            if letra != " " or self.nombre:  # Evita múltiples espacios iniciales
                self.nombre += letra
        elif self.modo_actual == "cantidad":
            numero = self.numeros[self.indice_numero]
            self.cantidad += numero
        self.mostrar_estado()

    def procesar_finalizacion(self):
        """Procesa la finalización de un paso o del flujo completo."""
        if self.modo_actual == "nombre":
            self.modo_actual = "cantidad"
        elif self.modo_actual == "cantidad":
            self.modo_actual = "tipo"
        elif self.modo_actual == "tipo":
            self.modo_actual = "confirmar"
        elif self.modo_actual == "confirmar" and self.confirmacion == 1:
            self.enviar_datos()
        else:
            self.reiniciar()  # Si se selecciona "No" en la confirmación
        self.mostrar_estado()

    def mostrar_estado(self):
        """Actualiza el LCD con el estado actual."""
        self.lcd.clear()
        if self.modo_actual == "nombre":
            letra_actual = self.alfabeto[self.indice_letra]
            self.lcd.write(f"Nombre:", line=1)
            self.lcd.write(f"{self.nombre}{letra_actual}", line=2)
        elif self.modo_actual == "cantidad":
            numero_actual = self.numeros[self.indice_numero]
            self.lcd.write(f"Cantidad (g):", line=1)
            self.lcd.write(f"{self.cantidad}{numero_actual}", line=2)
        elif self.modo_actual == "tipo":
            tipo_actual = self.tipos_azucar[self.tipo_actual]
            self.lcd.write(f"Tipo de azúcar:", line=1)
            self.lcd.write(f"{tipo_actual}", line=2)
        elif self.modo_actual == "confirmar":
            opciones = ["No", "Sí"]
            self.lcd.write("Enviar datos?", line=1)
            self.lcd.write(opciones[self.confirmacion], line=2)

    def enviar_datos(self):
        """Envía los datos a la base de datos."""
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            # Inserta los datos en la tabla
            query = """
            INSERT INTO usuarios (nombre, cantidad, tipo_azucar)
            VALUES (%s, %s, %s)
            """
            valores = (self.nombre.strip(), self.cantidad.strip(), self.tipos_azucar[self.tipo_actual])
            cursor.execute(query, valores)
            conexion.commit()

            self.lcd.clear()
            self.lcd.write("Datos guardados", line=1)
            self.lcd.write("¡Gracias!", line=2)
            time.sleep(2)
        except mysql.connector.Error as e:
            self.lcd.clear()
            self.lcd.write("Error en BD", line=1)
            time.sleep(2)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
            self.reiniciar()

    def reiniciar(self):
        """Reinicia el flujo completo."""
        self.modo_actual = "nombre"
        self.finalizado = False
        self.nombre = ""
        self.cantidad = ""
        self.tipo_actual = 0
        self.confirmacion = 0
        self.indice_letra = 0
        self.indice_numero = 0
        self.mostrar_estado()

    def run(self):
        """Mantiene la clase activa."""
        while not self.finalizado:
            time.sleep(0.1)
