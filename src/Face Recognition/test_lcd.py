from RPLCD.i2c import CharLCD
from time import sleep

# Configuración del LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)

try:
    # Limpiar la pantalla al iniciar
    lcd.clear()
    
    # Escribir un mensaje en el LCD
    lcd.write_string("Hola, Mundo!")
    sleep(2)
    
    # Mostrar un segundo mensaje
    lcd.clear()
    lcd.write_string("LCD I2C Funciona")
    sleep(2)

    # Bucle para mostrar un contador
    lcd.clear()
    for i in range(10):
        lcd.write_string(f"Contador: {i}")
        sleep(3)
        lcd.clear()

except KeyboardInterrupt:
    print("Interrupción manual.")

finally:
    # Limpiar la pantalla al salir
    lcd.clear()
    print("Prueba finalizada.")