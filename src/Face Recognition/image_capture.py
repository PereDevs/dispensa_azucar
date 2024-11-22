import os
from datetime import datetime
from picamera2 import Picamera2
from model_training import *
import time

# Cambiar este valor al nombre de la persona
  

import os

def create_folder(name):
    # Especificar la ruta completa
    dataset_folder = "/home/admin/dispensa_azucar/src/Face Recognition/dataset"
    
    # Crear la carpeta dataset si no existe
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    # Crear la carpeta específica de la persona dentro de dataset
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    
    return person_folder


def capture_photos(name, max_photos=5, delay_between_photos=2):
    """
    Captura fotos de una persona con Picamera2 y las guarda en un folder.
    :param name: Nombre de la persona.
    :param max_photos: Número máximo de fotos a capturar.
    :param delay_between_photos: Tiempo en segundos entre capturas.
    """
    folder = create_folder(name)
    
    # Inicializar la cámara
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
    picam2.start()

    # Permitir que la cámara se caliente
    time.sleep(2)

    photo_count = 0
    print(f"[INFO] Iniciando captura de fotos para {name}. Capturando {max_photos} fotos con {delay_between_photos}s de intervalo.")
    
    try:
        while photo_count < max_photos:
            # Capturar un frame de la cámara
            frame = picam2.capture_array()

            # Guardar la imagen con un timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                # Guardar la imagen como archivo JPEG
                from PIL import Image
                image = Image.fromarray(frame)
                image.save(f, format="JPEG")
            photo_count += 1
            print(f"[INFO] Foto {photo_count} guardada: {filepath}")

            # Esperar antes de la próxima captura
            time.sleep(delay_between_photos)
    
    except KeyboardInterrupt:
        print("[INFO] Captura interrumpida por el usuario.")
    
    finally:
        # Detener la cámara
        picam2.stop()
        print(f"[INFO] Captura completada. Total de fotos guardadas: {photo_count}.")

if __name__ == "__main__":
    pname =input("Nombre:")
    papellidos = input("Apellidos:")
    pid = input("Dame un ID para test:")
    pnameall = pname.lower()+papellidos.lower()
    
    # Temporizador de cuenta atrás antes de la captura
    countdown = 5  # Número de segundos para la cuenta atrás
    print(f"Voy a capturar unas fotos tuyas en: {countdown} segundos.")
    for i in range(countdown, 0, -1):
        print(f"{i}...")  # Imprimir el tiempo restante
        time.sleep(1)  # Esperar 1 segundo entre cada número

    # Mensaje final antes de iniciar la captura
    print("¡Capturando las fotos ahora!")
    
    
    capture_photos(name=pnameall,  max_photos=5, delay_between_photos=2)
    procesar_persona(pnameall,pid)
