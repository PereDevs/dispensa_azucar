import os
from datetime import datetime
from picamera2 import Picamera2
from model_training import procesar_persona
import time
from PIL import Image
import smbus
import RPi.GPIO as GPIO

# Configuración de la dirección del LCD y los pines GPIO
I2C_ADDR = 0x27  # Cambia esta dirección si tu LCD usa otra
LCD_WIDTH = 16   # Tamaño del LCD (16x2)
LCD_LINE_1 = 0x80  # Dirección para la primera línea
LCD_LINE_2 = 0xC0  # Dirección para la segunda línea
ENABLE = 0b00000100  # Enable bit
BACKLIGHT = 0x08     # Encender luz de fondo

# Pines GPIO para los LEDs
LED_RED = 17
LED_GREEN = 27
LED_WHITE = 22

# Inicializar GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_WHITE, GPIO.OUT)

# Controlar el LCD mediante I2C
class LCD:
    def __init__(self, address=I2C_ADDR):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.init_lcd()

    def init_lcd(self):
        """Inicializa el LCD."""
        self.lcd_byte(0x33, 0)
        self.lcd_byte(0x32, 0)
        self.lcd_byte(0x06, 0)
        self.lcd_byte(0x0C, 0)
        self.lcd_byte(0x28, 0)
        self.lcd_clear()

    def lcd_clear(self):
        """Limpia el contenido del LCD."""
        self.lcd_byte(0x01, 0)

    def lcd_byte(self, bits, mode):
        """Envía datos o comandos al LCD."""
        high_bits = mode | (bits & 0xF0) | BACKLIGHT
        low_bits = mode | ((bits << 4) & 0xF0) | BACKLIGHT
        self.bus.write_byte(self.address, high_bits)
        self.lcd_toggle_enable(high_bits)
        self.bus.write_byte(self.address, low_bits)
        self.lcd_toggle_enable(low_bits)

    def lcd_toggle_enable(self, bits):
        """Activa el bit ENABLE."""
        time.sleep(0.0005)
        self.bus.write_byte(self.address, (bits | ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.address, (bits & ~ENABLE))
        time.sleep(0.0005)

    def write(self, message, line=LCD_LINE_1):
        """Escribe un mensaje en el LCD."""
        self.lcd_byte(line, 0)
        for char in message.ljust(LCD_WIDTH, " "):
            self.lcd_byte(ord(char), 1)

# Instancias para el LCD y configuración inicial
lcd = LCD()
GPIO.output(LED_RED, GPIO.LOW)
GPIO.output(LED_GREEN, GPIO.LOW)
GPIO.output(LED_WHITE, GPIO.LOW)

def create_folder(user_id):
    """Crea la carpeta para un usuario basado en su ID."""
    dataset_folder = "/home/admin/dispensa_azucar/src/Face Recognition/dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    person_folder = os.path.join(dataset_folder, str(user_id))
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def capture_photos(name, user_id, max_photos=5, delay_between_photos=2):
    """
    Captura fotos del usuario y las guarda en su carpeta.
    """
    folder = create_folder(user_id)

    # Inicializar la cámara
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
    picam2.start()
    time.sleep(2)

    # Mostrar mensaje en LCD y encender LED rojo
    lcd.write("Capturando...")
    GPIO.output(LED_RED, GPIO.HIGH)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_WHITE, GPIO.LOW)

    photo_count = 0
    print(f"[INFO] Iniciando captura de fotos para {name} con ID {user_id}.")
    
    try:
        while photo_count < max_photos:
            frame = picam2.capture_array()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{user_id}_{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as f:
                image = Image.fromarray(frame)
                image.save(f, format="JPEG")

            photo_count += 1
            print(f"[INFO] Foto {photo_count} guardada: {filepath}")
            time.sleep(delay_between_photos)
    
    except KeyboardInterrupt:
        print("[INFO] Captura interrumpida.")
    
    finally:
        picam2.stop()
        print(f"[INFO] Captura completada. Total de fotos guardadas: {photo_count}.")
    return photo_count

if __name__ == "__main__":
    pname = input("Nombre: ")
    pid = input("ID: ")
    pnameall = pname.lower()
    
    countdown = 5
    print(f"Captura en: {countdown} segundos.")
    for i in range(countdown, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # Captura nuevas fotos
    nuevas_fotos = capture_photos(name=pnameall, user_id=pid, max_photos=5, delay_between_photos=2)

    if nuevas_fotos > 0:
        print("[INFO] Añadiendo encodings de nuevas imágenes.")
        
        # Mostrar mensaje en LCD y mantener LED rojo encendido
        lcd.write(f"Analizando a")
        lcd.write(f"{pnameall}", LCD_LINE_2)

        GPIO.output(LED_RED, GPIO.HIGH)
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_WHITE, GPIO.LOW)
        
        procesar_persona(name=pnameall, user_id=pid)
        
        # Mostrar mensaje en LCD y encender LED verde
        lcd.write(f"{pnameall}")
        lcd.write("registro OK",LCD_LINE_2)

        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_WHITE, GPIO.LOW)
        time.sleep(5)
        GPIO.output(LED_GREEN, GPIO.LOW)
        lcd.lcd_clear()

    else:
        print("[INFO] No hay nuevas imágenes para añadir.")
        # Apagar LEDs si no se realiza ninguna acción
        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_WHITE, GPIO.LOW)