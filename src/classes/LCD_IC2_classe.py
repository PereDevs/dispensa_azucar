import smbus
import time

# Configuración del LCD
I2C_ADDR = 0x27  # Dirección I2C del módulo LCD
LCD_WIDTH = 16   # Máximo de caracteres por línea del LCD

# Modo de operación del LCD
LCD_CHR = 1  # Modo de datos
LCD_CMD = 0  # Modo de comando

# Direcciones RAM del LCD para líneas
LCD_LINE_1 = 0x80  # Dirección RAM para la línea 1
LCD_LINE_2 = 0xC0  # Dirección RAM para la línea 2

# Configuración de retroiluminación
LCD_BACKLIGHT = 0x08  # Encender retroiluminación
LCD_NOBACKLIGHT = 0x00  # Apagar retroiluminación

# Señales de control
ENABLE = 0b00000100  # Señal de habilitación

# Tiempos de espera
E_PULSE = 0.0005
E_DELAY = 0.0005

class LCD:
    def __init__(self, address=I2C_ADDR):
        self.address = address
        self.bus = smbus.SMBus(1)  # Interfaz I2C en la Raspberry Pi
        self.backlight = LCD_BACKLIGHT  # Retroiluminación activa por defecto
        self.init_lcd()

    def init_lcd(self):
        """Inicializa el LCD en modo 4 bits."""
        self.lcd_byte(0x33, LCD_CMD)  # Inicialización al modo 4 bits
        self.lcd_byte(0x32, LCD_CMD)  # Configuración del modo 4 bits
        self.lcd_byte(0x06, LCD_CMD)  # Modo de entrada
        self.lcd_byte(0x0C, LCD_CMD)  # Encender el display, sin cursor
        self.lcd_byte(0x28, LCD_CMD)  # Modo de 2 líneas, 5x8 matriz
        self.clear()

    def lcd_byte(self, bits, mode):
        """Envia datos o comandos al LCD."""
        high_bits = mode | (bits & 0xF0) | self.backlight
        low_bits = mode | ((bits << 4) & 0xF0) | self.backlight

        # Enviar datos altos
        self.bus.write_byte(self.address, high_bits)
        self.lcd_toggle_enable(high_bits)

        # Enviar datos bajos
        self.bus.write_byte(self.address, low_bits)
        self.lcd_toggle_enable(low_bits)

    def lcd_toggle_enable(self, bits):
        """Activa el bit de habilitación del LCD."""
        time.sleep(E_DELAY)
        self.bus.write_byte(self.address, (bits | ENABLE))
        time.sleep(E_PULSE)
        self.bus.write_byte(self.address, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def write(self, message, line):
        """Escribe un mensaje en la línea especificada."""
        self.lcd_byte(line, LCD_CMD)
        for char in message.ljust(LCD_WIDTH, " "):
            self.lcd_byte(ord(char), LCD_CHR)

    def clear(self):
        """Limpia la pantalla del LCD."""
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)

    def set_backlight(self, state):
        """Activa o desactiva la retroiluminación del LCD."""
        self.backlight = LCD_BACKLIGHT if state else LCD_NOBACKLIGHT
        self.bus.write_byte(self.address, 0x00)  # Forzar actualización
