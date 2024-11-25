import os
import pickle
from imutils import paths
import face_recognition
import cv2

class ModeloEntrenamiento:
    def __init__(self, dataset_path, encodings_path):
        """
        Inicializa la clase para el manejo del modelo.
        :param dataset_path: Ruta al directorio de imágenes del dataset.
        :param encodings_path: Ruta al archivo pickle donde se guardarán los encodings.
        """
        self.dataset_path = dataset_path
        self.encodings_path = encodings_path
        self.known_encodings = []
        self.known_names = []
        self.known_ids = []
        self.cargar_encodings()

    def cargar_encodings(self):
        """Carga los encodings existentes desde el archivo pickle."""
        if os.path.exists(self.encodings_path):
            try:
                with open(self.encodings_path, "rb") as f:
                    data = pickle.load(f)
                    self.known_encodings = data.get("encodings", [])
                    self.known_names = data.get("names", [])
                    self.known_ids = data.get("ids", [])
                print("[INFO] Encodings cargados correctamente.")
            except Exception as e:
                print(f"[ERROR] No se pudieron cargar los encodings existentes: {e}")

    def procesar_imagenes(self, nombre, user_id):
        """
        Procesa las imágenes de un usuario y actualiza los encodings.
        :param nombre: Nombre del usuario.
        :param user_id: ID único del usuario.
        """
        user_folder = os.path.join(self.dataset_path, str(user_id))
        if not os.path.exists(user_folder):
            print(f"[ERROR] El directorio {user_folder} no existe.")
            return

        print(f"[INFO] Procesando imágenes del usuario {nombre} (ID: {user_id}) en {user_folder}.")
        image_paths = list(paths.list_images(user_folder))
        if not image_paths:
            print(f"[ERROR] No se encontraron imágenes en {user_folder}.")
            return

        for (i, image_path) in enumerate(image_paths):
            print(f"[INFO] Procesando imagen {i + 1}/{len(image_paths)}: {image_path}")
            image = cv2.imread(image_path)
            if image is None:
                print(f"[WARNING] La imagen {image_path} no pudo ser cargada.")
                continue

            try:
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb, model="hog")  # Cambia a "cnn" si tienes GPU
                encodings = face_recognition.face_encodings(rgb, boxes)
                for encoding in encodings:
                    self.known_encodings.append(encoding)
                    self.known_names.append(nombre)
                    self.known_ids.append(user_id)
            except Exception as e:
                print(f"[WARNING] Error procesando {image_path}: {e}")

        self.serializar_encodings()

    def serializar_encodings(self):
        """Serializa los encodings actuales en un archivo pickle."""
        data = {
            "encodings": self.known_encodings,
            "names": self.known_names,
            "ids": self.known_ids
        }
        try:
            with open(self.encodings_path, "wb") as f:
                pickle.dump(data, f)
            print(f"[INFO] Encodings guardados correctamente en {self.encodings_path}.")
        except Exception as e:
            print(f"[ERROR] No se pudieron guardar los encodings: {e}")
