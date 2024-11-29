from gpiozero import Button
from time import sleep

class EntradaNombre:
    def __init__(self, pin_boton_adelante, pin_boton_atras, pin_boton_confirmar, lcd):
        self.boton_adelante = Button(pin_boton_adelante)
        self.boton_atras = Button(pin_boton_atras)
        self.boton_confirmar = Button(pin_boton_confirmar, hold_time=3)
        self.lcd = lcd
        self.alfabeto = " " + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Inicia con un espacio
        self.indice_letra = 0
        self.nombre = ""
        self.enviando = False

        # Asignar eventos a los botones
        self.boton_adelante.when_pressed = self.mover_adelante
        self.boton_atras.when_pressed = self.mover_atras
        self.boton_confirmar.when_pressed = self.confirmar_letra
        self.boton_confirmar.when_held = self.enviar_nombre

        self.mostrar_estado()

    def mover_adelante(self):
        if not self.enviando:
            self.indice_letra = (self.indice_letra + 1) % len(self.alfabeto)
            self.mostrar_estado()

    def mover_atras(self):
        if not self.enviando:
            self.indice_letra = (self.indice_letra - 1) % len(self.alfabeto)
            self.mostrar_estado()

    def confirmar_letra(self):
        """Confirma la letra seleccionada y la añade al nombre."""
        if not self.enviando:
            letra = self.alfabeto[self.indice_letra]
            if letra != " " or self.nombre:  # Evita múltiples espacios iniciales
                self.nombre += letra
            self.indice_letra = 0  # Reinicia a un espacio en blanco
            self.mostrar_estado()

    def enviar_nombre(self):
        """Envía el nombre completo al mantener el botón presionado."""
        if not self.enviando:
            self.enviando = True
            self.lcd.clear()
            self.lcd.write(f"Enviado: {self.nombre}",line=1)
            sleep(3)  # Pausa para que el usuario vea el nombre enviado
            self.nombre = ""  # Reinicia el nombre después de enviarlo
            self.indice_letra = 0
            self.enviando = False
            self.mostrar_estado()

    def borrar_nombre(self):
        """Borra el nombre actual y reinicia el proceso."""
        self.nombre = ""
        self.indice_letra = 0
        self.mostrar_estado()

    def mostrar_estado(self):
        """Muestra el estado actual en el LCD."""
        letra_actual = self.alfabeto[self.indice_letra]
        self.lcd.clear()
        self.lcd.write(f"Nombre: {self.nombre}{letra_actual}", line=1)  # Mostrar todo en la línea 1

    def run(self):
        """Método para mantener la clase activa."""
        try:
            while True:
                # Si ambos botones (adelante y atrás) se presionan simultáneamente, borra el nombre
                if self.boton_adelante.is_pressed and self.boton_atras.is_pressed:
                    self.borrar_nombre()
                sleep(0.1)  # Reducir la carga de la CPU
        except KeyboardInterrupt:
            print("Saliendo...")