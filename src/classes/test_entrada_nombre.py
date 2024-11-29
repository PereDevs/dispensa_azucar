from LCD_IC2_classe import LCD_I2C
from Entrada_Nombre_Classe import EntradaDatos

# Configuración de pines
PIN_BOTON_ADELANTE = 18
PIN_BOTON_ATRAS = 19
PIN_BOTON_CONFIRMAR = 13

# Crear LCD
lcd = LCD_I2C()

# Crear instancia para introducir un nombre
entrada_nombre = EntradaDatos(
    pin_boton_adelante=PIN_BOTON_ADELANTE,
    pin_boton_atras=PIN_BOTON_ATRAS,
    pin_boton_confirmar=PIN_BOTON_CONFIRMAR,
    lcd=lcd,
    modo="tipo"  # Cambia a "cantidad" o "tipo" según lo necesario
)

# Iniciar
entrada_nombre.run()