from gpiozero import Button
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

        # Asignar eventos a los botones
        self.boton_adelante.when_pressed = self.mover_adelante
        self.boton_atras.when_pressed = self.mover_atras
        self.boton_confirmar.when_pressed = self.confirmar_opcion
        self.boton_confirmar.when_held = self.enviar_datos

        self.mostrar_estado()

    def mover_adelante(self):
        if not self.enviando:
            if self.modo == "nombre":
                self.indice_letra = (self.indice_letra + 1) % len(self.alfabeto)
                time.sleep(0.02)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra + 1) % len(self.numeros)
                time.sleep(0.02)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo + 1) % len(self.tipos_azucar)
                time.sleep(0.02)
            self.mostrar_estado()

    def mover_atras(self):
        if not self.enviando:
            if self.modo == "nombre":
                self.indice_letra = (self.indice_letra - 1) % len(self.alfabeto)
                time.sleep(0.02)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra - 1) % len(self.numeros)
                time.sleep(0.02)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo - 1) % len(self.tipos_azucar)
                time.sleep(0.02)
            self.mostrar_estado()

    def confirmar_opcion(self):
        if not self.enviando:
            if self.modo == "nombre":
                letra = self.alfabeto[self.indice_letra]
                print(f"[DEBUG] Letra seleccionada: {letra}")
                if letra != " " or self.nombre:  # Evita múltiples espacios iniciales
                    self.nombre += letra
                    print(f"[DEBUG] Nombre actual: {self.nombre}")
                self.indice_letra = 0  # Reinicia al espacio en blanco
            self.mostrar_estado()

    def enviar_datos(self):
        """Envía los datos según el modo actual."""
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
                tipo_valor = self.indice_tipo + 1  # Enviar 1, 2 o 3
                self.lcd.write(f"Tipo: {tipo_seleccionado}", line=1)
                self.lcd.write("OK!", line=2)
            time.sleep(3)
            self.reiniciar_datos()
            self.mostrar_estado()

    def reiniciar_datos(self):
        """Reinicia los datos según el modo."""
        if self.modo == "nombre":
            self.nombre = ""
        elif self.modo == "cantidad":
            self.cantidad = ""
        elif self.modo == "tipo":
            self.indice_tipo = 0
        self.indice_letra = 0
        self.enviando = False

    def mostrar_estado(self):
        """Muestra el estado actual en el LCD."""
        self.lcd.clear()
        if self.modo == "nombre":
            letra_actual = self.alfabeto[self.indice_letra]
            self.lcd.write(f"Nombre: {self.nombre}{letra_actual}", line=1)
        elif self.modo == "cantidad":
            numero_actual = self.numeros[self.indice_letra]
            self.lcd.write(f"Cantidad:{self.cantidad}{numero_actual}", line=1)
        elif self.modo == "tipo":
            tipo_actual = self.tipos_azucar[self.indice_tipo]
            self.lcd.write(f"Tipo: {tipo_actual}", line=1)

    def run(self):
        """Mantiene la clase activa."""
        try:
            while True:
                # Si ambos botones (adelante y atrás) se presionan simultáneamente, reinicia los datos
                if self.boton_adelante.is_pressed and self.boton_atras.is_pressed:
                    self.reiniciar_datos()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Saliendo...")