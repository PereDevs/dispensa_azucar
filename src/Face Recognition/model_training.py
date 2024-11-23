import os
from imutils import paths
import face_recognition
import pickle
import cv2

def procesar_persona(name, user_id, path="/home/admin/dispensa_azucar/src/Face Recognition/dataset"):
    """
    Procesa las imágenes de una persona en un dataset, calcula los encodings y los guarda en un archivo pickle.
    Cada encoding se guarda con su ID y nombre.
    """
    dataset_path = os.path.join(path, user_id)
    encodings_path = os.path.join(path, "encodings.pickle")
    processed_file = os.path.join(dataset_path, "processed_images.txt")

    print(f"[INFO] Entrenando para la persona: {name}")
    print(f"Dataset path: {dataset_path}")
    print(f"Encodings will be saved to: {encodings_path}")

    # Verificar si el dataset existe
    if not os.path.exists(dataset_path):
        print(f"[ERROR] El directorio {dataset_path} no existe.")
        return

    print("[INFO] Start processing faces...")
    imagePaths = list(paths.list_images(dataset_path))

    # Verificar si se encontraron imágenes
    if not imagePaths:
        print("[ERROR] No se encontraron imágenes en el dataset.")
        return

    # Cargar imágenes ya procesadas desde el archivo processed_images.txt
    processed_images = set()
    if os.path.exists(processed_file):
        with open(processed_file, "r") as f:
            processed_images = set(f.read().strip().splitlines())

    # Cargar encodings existentes si el archivo pickle ya existe
    existing_data = []
    if os.path.exists(encodings_path):
        print("[INFO] Cargando encodings existentes...")
        with open(encodings_path, "rb") as f:
            existing_data = pickle.load(f)

    # Procesar cada imagen
    new_processed_images = []
    for (i, imagePath) in enumerate(imagePaths):
        image_name = os.path.basename(imagePath)
        if image_name in processed_images:
            print(f"[INFO] Imagen ya procesada, saltando: {image_name}")
            continue

        print(f"[INFO] Processing image {i + 1}/{len(imagePaths)}: {imagePath}")
        
        # Cargar la imagen y convertir a RGB
        image = cv2.imread(imagePath)
        if image is None:
            print(f"[WARNING] La imagen {imagePath} no pudo ser cargada.")
            continue

        try:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detectar los rostros y calcular sus encodings
            boxes = face_recognition.face_locations(rgb, model="hog")  # Cambia a "cnn" si tienes GPU
            encodings = face_recognition.face_encodings(rgb, boxes)
        except Exception as e:
            print(f"[WARNING] Error procesando {imagePath}: {e}")
            continue

        # Guardar los datos de cada encoding
        for encoding in encodings:
            existing_data.append({
                "encoding": encoding,
                "name": name,  # Aquí aseguramos que sea el nombre de la persona
                "id": user_id
            })

        # Registrar la imagen como procesada
        new_processed_images.append(image_name)

    # Actualizar el archivo processed_images.txt solo si hay nuevas imágenes procesadas
    if new_processed_images:
        with open(processed_file, "a") as f:
            for image_name in new_processed_images:
                f.write(f"{image_name}\n")

    # Serializar los encodings en un archivo
    print("[INFO] Serializing encodings...")
    with open(encodings_path, "wb") as f:
        pickle.dump(existing_data, f)

    print(f"[INFO] Training complete. Encodings saved to '{encodings_path}'")