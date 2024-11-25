import os
from imutils import paths
import face_recognition
import pickle
import cv2

def procesar_persona(name, user_id, path="/home/admin/dispensa_azucar/dataset"):
    """
    Procesa las imágenes de una persona en un dataset, calcula los encodings y los guarda en un archivo pickle.
    """
    dataset_path = os.path.join(path, str(user_id))
    encodings_path = os.path.join(path, "encodings.pickle")
    processed_file = os.path.join(dataset_path, "processed_images.txt")

    print(f"[INFO] Entrenando para la persona: {name}")
    print(f"Dataset path: {dataset_path}")
    print(f"Encodings will be saved to: {encodings_path}")

    if not os.path.exists(dataset_path):
        print(f"[ERROR] El directorio {dataset_path} no existe.")
        return

    print("[INFO] Start processing faces...")
    imagePaths = list(paths.list_images(dataset_path))

    if not imagePaths:
        print("[ERROR] No se encontraron imágenes en el dataset.")
        return

    # Procesar encodings existentes
    existing_data = []
    if os.path.exists(encodings_path):
        with open(encodings_path, "rb") as f:
            existing_data = pickle.load(f)

    for (i, imagePath) in enumerate(imagePaths):
        print(f"[INFO] Processing image {i + 1}/{len(imagePaths)}: {imagePath}")
        image = cv2.imread(imagePath)
        if image is None:
            print(f"[WARNING] No se pudo cargar la imagen {imagePath}")
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            existing_data.append({"id": user_id, "name": name, "encoding": encoding})

    print("[INFO] Serializing encodings...")
    with open(encodings_path, "wb") as f:
        pickle.dump(existing_data, f)

    print(f"[INFO] Training complete. Encodings saved to '{encodings_path}'")