from LCD_IC2_classe import LCD_I2C
from Entrada_Nombre_Classe import EntradaNombre  # Asegúrate de que esta clase esté en el archivo correcto

# Configurar los pines GPIO de los botones
PIN_BOTON_ADELANTE = 18
PIN_BOTON_ATRAS = 19
PIN_BOTON_CONFIRMAR = 13

# Crear una instancia del LCD (ajusta si tu clase LCD tiene otro constructor)
lcd = LCD_I2C()

# Crear la instancia de la clase EntradaNombre
entrada_nombre = EntradaNombre(
    pin_boton_adelante=PIN_BOTON_ADELANTE,
    pin_boton_atras=PIN_BOTON_ATRAS,
    pin_boton_confirmar=PIN_BOTON_CONFIRMAR,
    lcd=lcd
)
try:
# Ejecutar el método run para iniciar la entrada de nombre
    entrada_nombre.run()
except KeyboardInterrupt:
    lcd.clear()