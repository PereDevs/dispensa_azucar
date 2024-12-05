import RPi.GPIO as GPIO
import time

class EntradaDatos:
    def __init__(self, pin_boton_adelante, pin_boton_atras, pin_boton_confirmar, lcd, modo):
        """
        :param modo: Puede ser 'nombre', 'cantidad' o 'tipo'.
        """
        self.boton_adelante = pin_boton_adelante
        self.boton_atras = pin_boton_atras
        self.boton_confirmar = pin_boton_confirmar
        self.lcd = lcd

        # Modos
        self.modo = modo
        self.nombre = ""
        self.cantidad = ""
        self.tipos_azucar = ["Blanco", "Moreno", "Edulcorante"]
        self.indice_tipo = 0
        self.numeros = "0123456789."
        self.alfabeto = " " + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.indice_letra = 0
        self.enviando = False

        # Configuración de pines
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.boton_adelante, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boton_atras, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boton_confirmar, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.mostrar_estado()

    def mover_adelante(self, channel):
        if not self.enviando:
            if self.modo == "registro":
                self.indice_tipo = (self.indice_tipo + 1) % 2  # Alternar entre 0 y 1
            elif self.modo == "nombre":
                self.indice_letra = (self.indice_letra + 1) % len(self.alfabeto)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra + 1) % len(self.numeros)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo + 1) % len(self.tipos_azucar)
            self.mostrar_estado()

    def mover_atras(self, channel):
        if not self.enviando:
            if self.modo == "registro":
                self.indice_tipo = (self.indice_tipo - 1) % 2  # Alternar entre 0 y 1
            elif self.modo == "nombre":
                self.indice_letra = (self.indice_letra - 1) % len(self.alfabeto)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra - 1) % len(self.numeros)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo - 1) % len(self.tipos_azucar)
            self.mostrar_estado()

    def confirmar_opcion(self, channel):
        if not self.enviando:
            if self.modo == "nombre":
                letra = self.alfabeto[self.indice_letra]
                if letra != " " or self.nombre:  # Evita múltiples espacios iniciales
                    self.nombre += letra
                self.indice_letra = 0  # Reinicia al espacio en blanco
            elif self.modo == "registro":
                opciones = ["Sí", "No"]
                seleccion = opciones[self.indice_tipo]
                self.cantidad = str(self.indice_tipo)  # Índice 0 = No, Índice 1 = Sí
                self.enviando = True  # Finaliza el proceso
            self.mostrar_estado()

    def enviar_datos(self, channel):
        if not self.enviando:
            self.enviando = True
            self.lcd.clear()
            if self.modo == "nombre":
                self.lcd.write(f":{self.nombre}", line=1)
                self.lcd.write("OK!", line=2)
            elif self.modo == "cantidad":
                self.lcd.write(f"Cantidad:OK -  {self.cantidad}", line=1)
                self.lcd.write("OK!", line=2)
            elif self.modo == "tipo":
                tipo_seleccionado = self.tipos_azucar[self.indice_tipo]
                self.lcd.write(f"Tipo: {tipo_seleccionado}", line=1)
                self.lcd.write("OK!", line=2)
            time.sleep(3)
            self.reiniciar_datos()
            self.mostrar_estado()

    def reiniciar_datos(self):
        if self.modo == "nombre":
            self.nombre = ""
        elif self.modo == "cantidad":
            self.cantidad = ""
        elif self.modo == "tipo":
            self.indice_tipo = 0
        self.indice_letra = 0
        self.enviando = False

    def mostrar_estado(self):
        self.lcd.clear()
        if self.modo == "registro":
            opciones = ["SI", "NO"]
            opcion_actual = opciones[self.indice_tipo]
            self.lcd.write("Registrarte?", line=1)
            self.lcd.write(f"{opcion_actual}", line=2)
        elif self.modo == "nombre":
            letra_actual = self.alfabeto[self.indice_letra]
            self.lcd.write("Nombre:", line=1)
            self.lcd.write(f"{self.nombre}{letra_actual}", line=2)
        elif self.modo == "cantidad":
            numero_actual = self.numeros[self.indice_letra]
            self.lcd.write("Cantidad:", line=1)
            self.lcd.write(f"{self.cantidad}{numero_actual}", line=2)
        elif self.modo == "tipo":
            tipo_actual = self.tipos_azucar[self.indice_tipo]
            self.lcd.write("Tipo:", line=1)
            self.lcd.write(f"{tipo_actual}", line=2)

    def run(self):
        GPIO.add_event_detect(self.boton_adelante, GPIO.FALLING, callback=self.mover_adelante, bouncetime=200)
        GPIO.add_event_detect(self.boton_atras, GPIO.FALLING, callback=self.mover_atras, bouncetime=200)
        GPIO.add_event_detect(self.boton_confirmar, GPIO.FALLING, callback=self.confirmar_opcion, bouncetime=200)

        try:
            while True:
                if GPIO.input(self.boton_adelante) == GPIO.LOW and GPIO.input(self.boton_atras) == GPIO.LOW:
                    self.reiniciar_datos()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Saliendo...")
        finally:
            GPIO.cleanup()
