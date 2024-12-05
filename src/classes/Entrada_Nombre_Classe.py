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
        self.finalizado = False  # Indicador de finalización del modo

        # Asignar eventos a los botones
        self.boton_adelante.when_pressed = self.mover_adelante
        self.boton_atras.when_pressed = self.mover_atras
        self.boton_confirmar.when_pressed = self.confirmar_opcion
        self.boton_confirmar.when_held = self.enviar_datos

    def mover_adelante(self):
        if not self.enviando:
            print(f"[DEBUG] Botón adelante presionado en modo: {self.modo}")
            if self.modo == "nombre":
                self.indice_letra = (self.indice_letra + 1) % len(self.alfabeto)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra + 1) % len(self.numeros)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo + 1) % len(self.tipos_azucar)
            self.mostrar_estado()

    def mover_atras(self):
        if not self.enviando:
            print(f"[DEBUG] Botón atrás presionado en modo: {self.modo}")
            if self.modo == "nombre":
                self.indice_letra = (self.indice_letra - 1) % len(self.alfabeto)
            elif self.modo == "cantidad":
                self.indice_letra = (self.indice_letra - 1) % len(self.numeros)
            elif self.modo == "tipo":
                self.indice_tipo = (self.indice_tipo - 1) % len(self.tipos_azucar)
            self.mostrar_estado()

    def confirmar_opcion(self):
        if not self.enviando:
            print(f"[DEBUG] Botón confirmar presionado en modo: {self.modo}")
            if self.modo == "nombre":
                letra = self.alfabeto[self.indice_letra]
                if letra != " " or self.nombre:  # Evita múltiples espacios iniciales
                    self.nombre += letra
                self.indice_letra = 0
            elif self.modo == "cantidad":
                numero = self.numeros[self.indice_letra]
                self.cantidad += numero
            elif self.modo == "tipo":
                pass  # En este caso, la selección ya está controlada por el índice
            self.mostrar_estado()

    def enviar_datos(self):
        """Envía los datos según el modo actual y marca el modo como finalizado."""
        if not self.enviando:
            self.enviando = True
            self.lcd.clear()

            if self.modo == "nombre":
                self.lcd.write(f"Nombre: {self.nombre}", line=1)
                self.lcd.write("OK!", line=2)
            elif self.modo == "cantidad":
                self.lcd.write(f"Cantidad: {self.cantidad}", line=1)
                self.lcd.write("OK!", line=2)
            elif self.modo == "tipo":
                tipo_seleccionado = self.tipos_azucar[self.indice_tipo]
                self.lcd.write(f"Tipo: {tipo_seleccionado}", line=1)
                self.lcd.write("OK!", line=2)

            time.sleep(2)
            self.finalizado = True  # Indica que el modo ha terminado
            print(f"[DEBUG] Finalizado establecido en enviar_datos: {self.finalizado}")

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
        print("[DEBUG] Datos reiniciados.")

    def mostrar_estado(self):
        """Muestra el estado actual en el LCD."""
        self.lcd.clear()
        print(f"[DEBUG] Mostrando estado para modo: {self.modo}")
        if self.modo == "nombre":
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
        """Ejecuta las acciones necesarias para el modo actual."""
        print(f"[DEBUG] Ejecutando run. Estado de finalizado: {self.finalizado}")
        if self.boton_adelante.is_pressed and self.boton_atras.is_pressed:
            self.reiniciar_datos()
            print("[DEBUG] Datos reiniciados en run.")
        time.sleep(0.1)
