from gpiozero import Button
import RPi.GPIO as GPIO
from LCD_IC2_classe import LCD_I2C
from Entrada_Nombre_Classe import EntradaDatos

# Configuración de pines GPIO
PIN_BOTON1 = 18  # Botón confirmar
PIN_BOTON2 = 19  # Botón avanzar
PIN_BOTON3 = 21  # Botón retroceder

# Limpieza previa de pines GPIO
try:
    GPIO.cleanup()
except RuntimeWarning:
    pass  # Ignora el error si ya están limpios

# Inicializar botones
button1 = Button(PIN_BOTON1)  # Confirmar
button2 = Button(PIN_BOTON2)  # Avanzar
button3 = Button(PIN_BOTON3)  # Retroceder

# Crear LCD
lcd = LCD_I2C()

# Crear instancia para introducir un nombre
entrada_nombre = EntradaDatos(
    pin_boton_adelante=button2,
    pin_boton_atras=button3,
    pin_boton_confirmar=button1,
    lcd=lcd,
    modo="nombre"  # Cambia a "cantidad" o "tipo" según lo necesario
)

# Agregar depuración al método confirmar_opcion
def confirmar_opcion_debug():
    """
    Método para probar confirmar_opcion con depuración.
    """
    print("[DEBUG] Método confirmar_opcion llamado")
    entrada_nombre.confirmar_opcion()
    print(f"[DEBUG] Nombre actual: {entrada_nombre.nombre}")

# Asignar el método de depuración al botón confirmar
button1.when_pressed = confirmar_opcion_debug

# Simulación de flujo para probar
print("[INFO] Presiona el botón CONFIRMAR para agregar la letra seleccionada.")
print("[INFO] Usa los botones ADELANTE y ATRÁS para cambiar la letra.")
print("[INFO] Observa el estado del nombre actual en la terminal y LCD.")

# Mantener el programa en ejecución para pruebas
try:
    entrada_nombre.run()
except KeyboardInterrupt:
    print("[INFO] Salida del programa.")
finally:
    GPIO.cleanup()
