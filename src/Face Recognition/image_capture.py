import os
from datetime import datetime
from picamera2 import Picamera2
from model_training import *
import time
from PIL import Image

def create_folder(id):
    """Crea la carpeta para un usuario basado en su ID."""
    dataset_folder = "/home/admin/dispensa_azucar/src/Face Recognition/dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    person_folder = os.path.join(dataset_folder, id)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def get_existing_images(folder):
    """Obtiene una lista de imágenes existentes en la carpeta."""
    return {file for file in os.listdir(folder) if file.endswith(".jpg")}

def get_processed_images(folder):
    """Lee el archivo de imágenes ya procesadas. Si no existe, lo crea vacío."""
    processed_file = os.path.join(folder, "processed_images.txt")
    if not os.path.exists(processed_file):
        # Si el archivo no existe, lo crea vacío
        open(processed_file, "w").close()
        return set()
    with open(processed_file, "r") as f:
        return set(f.read().strip().splitlines())

def save_processed_images(folder, processed_images):
    """Guarda todas las imágenes procesadas en el archivo."""
    processed_file = os.path.join(folder, "processed_images.txt")
    with open(processed_file, "w") as f:
        for image in sorted(processed_images):
            f.write(f"{image}\n")

def process_new_images(folder, id):
    """
    Procesa solo las imágenes nuevas y añade los encodings de las nuevas.
    """
    all_images = get_existing_images(folder)
    processed_images = get_processed_images(folder)
    new_images = all_images - processed_images

    if not new_images:
        print("[INFO] No hay imágenes nuevas para procesar.")
        return

    print(f"[INFO] Procesando {len(new_images)} imágenes nuevas.")

    for image_name in new_images:
        image_path = os.path.join(folder, image_name)
        try:
            # Llama a tu función de procesamiento de encodings
            procesar_persona(image_path, id)  # Ajusta según tu implementación
            print(f"[INFO] Procesado: {image_name}")
            # Agrega la imagen procesada al conjunto
            processed_images.add(image_name)
        except Exception as e:
            print(f"[ERROR] No se pudo procesar {image_name}: {e}")

    # Actualizar el archivo con todas las imágenes procesadas
    save_processed_images(folder, processed_images)
    print(f"[INFO] Registro actualizado. Total de imágenes procesadas: {len(processed_images)}.")

def capture_photos(name, id, max_photos=5, delay_between_photos=2):
    """
    Captura fotos del usuario y las guarda en su carpeta.
    """
    folder = create_folder(id)
    existing_images = get_existing_images(folder)

    # Inicializar la cámara
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
    picam2.start()
    time.sleep(2)

    photo_count = 0
    print(f"[INFO] Iniciando captura de fotos para {name} con ID {id}.")
    
    try:
        while photo_count < max_photos:
            frame = picam2.capture_array()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{id}_{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)

            if filename in existing_images:
                print(f"[INFO] Imagen duplicada: {filename}. Saltando.")
                continue

            with open(filepath, "wb") as f:
                image = Image.fromarray(frame)
                image.save(f, format="JPEG")

            photo_count += 1
            print(f"[INFO] Foto {photo_count} guardada: {filepath}")
            existing_images.add(filename)
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
    nuevas_fotos = capture_photos(name=pnameall, id=pid, max_photos=5, delay_between_photos=2)

    if nuevas_fotos > 0:
        print("[INFO] Añadiendo encodings de nuevas imágenes.")
        folder = create_folder(pid)
        process_new_images(folder, pid)
    else:
        print("[INFO] No hay nuevas imágenes para añadir.")