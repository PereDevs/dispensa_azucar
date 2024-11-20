from picamera2 import Picamera2
from PIL import Image, ImageOps
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import time

def capture_and_display():
    # Configuración de la cámara
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()

    # Capturar la imagen
    image_path = "captured_image.jpg"
    picam2.capture_file(image_path)
    print(f"Imagen capturada: {image_path}")
    picam2.stop()

    # Cargar y procesar la imagen
    image = Image.open(image_path).convert("L")  # Convertir a escala de grises
    image_resized = image.resize((128, 64))  # Ajustar al tamaño del OLED
    image_binary = image_resized.point(lambda x: 0 if x < 128 else 255, "1")  # Convertir a blanco y negro

    # Configuración del OLED
    serial = i2c(port=1, address=0x3C)  # Dirección típica del OLED I2C
    oled = ssd1306(serial)

    # Mostrar la imagen en el OLED
    oled.display(image_binary)
    print("Imagen mostrada en el OLED.")
    time.sleep(30)

if __name__ == "__main__":
    capture_and_display()
