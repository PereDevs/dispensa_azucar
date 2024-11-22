import os
from imutils import paths
import face_recognition
import pickle
import cv2

def procesar_persona(nombre, user_id, path="/home/admin/dispensa_azucar/src/Face Recognition/dataset"):
    """
    Procesa las imágenes de una persona en un dataset, calcula los encodings y los guarda en un archivo pickle.
    Se añade un ID único para cada usuario.
    :param path: Ruta base del dataset.
    :param nombre: Nombre de la persona a procesar.
    :param user_id: ID único del usuario.
    """
    # Construir la ruta del dataset para la persona
    dataset_path = os.path.join(path, nombre)
    
    # Ruta para guardar encodings.pickle en la carpeta dataset, fuera de la subcarpeta del usuario
    encodings_path = os.path.join(path, "encodings.pickle")

    print(f"[INFO] Entrenando para la persona: {nombre}")
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

    # Inicializar listas para nombres, encodings e IDs
    knownEncodings = []
    knownNames = []
    knownIDs = []

    # Verificar si ya existen encodings previos y cargarlos
    if os.path.exists(encodings_path):
        print("[INFO] Cargando encodings existentes...")
        with open(encodings_path, "rb") as f:
            data = pickle.load(f)
            knownEncodings = data.get("encodings", [])
            knownNames = data.get("names", [])
            knownIDs = data.get("ids", [])

    # Procesar cada imagen
    for (i, imagePath) in enumerate(imagePaths):
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

        # Agregar cada encoding junto con su nombre e ID
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(nombre)
            knownIDs.append(user_id)  # Añadir el ID del usuario

    # Serializar los encodings en un archivo
    print("[INFO] Serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames, "ids": knownIDs}
    with open(encodings_path, "wb") as f:
        pickle.dump(data, f)

    print(f"[INFO] Training complete. Encodings saved to '{encodings_path}'")

# Ejemplo de uso
#if __name__ == "__main__":
#    base_path = "/home/admin/dispensa_azucar/src/Face Recognition/dataset"
#    person_name = "Antonio"
#    user_id = 123  # ID único para el usuario Antonio (puedes cambiarlo)
#    procesar_persona(base_path, person_name, user_id)
