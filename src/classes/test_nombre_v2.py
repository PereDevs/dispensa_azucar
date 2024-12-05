from LCD_IC2_classe import LCD_I2C
from EntradaDatos_v2 import EntradaDatosCompletos

# Configuración de los pines GPIO
PIN_ADELANTE = 19
PIN_ATRAS = 21
PIN_CONFIRMAR = 18

# Configuración de la base de datos
DB_CONFIG = {
    'user': 'sugar',
    'password': '12345',
    'host': 'localhost',
    'database': 'sugardb'
}

# Inicializar el LCD y la clase de entrada de datos
lcd = LCD_I2C()
entrada_datos = EntradaDatosCompletos(PIN_ADELANTE, PIN_ATRAS, PIN_CONFIRMAR, lcd, DB_CONFIG)

# Ejecutar el flujo
try:
     entrada_datos.run()
except KeyboardInterrupt:
    print("[INFO] Salida del programa.")
finally:
    entrada_datos.reiniciar()
