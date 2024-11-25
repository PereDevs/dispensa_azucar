import os
import pickle
import cv2
import face_recognition


class ModeloEntrenamiento:
    def __init__(self, dataset_path, encodings_path):
        self.dataset_path = dataset_path
        self.encodings_path = encodings_path
        self.known_encodings = []
        self.known_names = []

        # Cargar encodings existentes si el archivo existe
        self.cargar_encodings()

    def cargar_encodings(self):
        """Carga los encodings desde el archivo."""
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data.get("encodings", [])
                self.known_names = data.get("names", [])
        else:
            print("[INFO] No se encontró archivo de encodings. Inicializando vacío.")
            self.known_encodings = []
            self.known_names = []

    def entrenar_usuario(self, nombre, id_usuario):
        """Agrega un usuario y sus encodings al modelo."""
        user_folder = os.path.join(self.dataset_path, str(id_usuario))
        image_paths = [os.path.join(user_folder, img) for img in os.listdir(user_folder) if img.endswith('.jpg')]

        for image_path in image_paths:
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                self.known_encodings.append(encoding)
                self.known_names.append(nombre)

        # Guardar encodings actualizados
        self.guardar_encodings()

    def guardar_encodings(self):
        """Guarda los encodings actuales en el archivo."""
        data = {"encodings": self.known_encodings, "names": self.known_names}
        with open(self.encodings_path, "wb") as f:
            pickle.dump(data, f)
        print("[INFO] Encodings guardados correctamente.")
