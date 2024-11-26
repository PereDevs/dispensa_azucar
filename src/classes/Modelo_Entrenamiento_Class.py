import pickle
import os
import cv2  # Para leer y procesar imágenes
import face_recognition  # Biblioteca para reconocimiento facial

class ModeloEntrenamiento:
    def __init__(self, dataset_path, encodings_path):
        self.dataset_path = dataset_path
        self.encodings_path = encodings_path
        self.known_encodings = []  # Lista para almacenar los encodings faciales
        self.known_ids = []        # Lista para almacenar los IDs de usuarios
        self.known_names = []      # Lista para almacenar los nombres de usuarios
        self.cargar_encodings()    # Cargar encodings existentes

    def cargar_encodings(self):
        """Carga los encodings desde el archivo, si existe."""
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data.get("encodings", [])
                self.known_ids = data.get("ids", [])  # Cargar IDs de usuarios
                self.known_names = data.get("names", [])  # Cargar nombres
                print("[INFO] Encodings cargados correctamente.")
        else:
            print("[INFO] No se encontró archivo de encodings. Inicializando vacío.")
            self.known_encodings = []
            self.known_ids = []  # Inicializar lista vacía para IDs
            self.known_names = []  # Inicializar lista vacía para nombres

    def guardar_encodings(self):
        """Guarda los encodings actuales en el archivo."""
        data = {
            "encodings": self.known_encodings,
            "ids": self.known_ids,  # Guardar IDs
            "names": self.known_names  # Guardar nombres
        }
        with open(self.encodings_path, "wb") as f:
            pickle.dump(data, f)
        print("[INFO] Encodings guardados correctamente.")

    def entrenar_usuario(self, id_usuario, nombre):
        """Entrena el modelo con un nuevo usuario."""
        user_folder = os.path.join(self.dataset_path, str(id_usuario))
        if not os.path.exists(user_folder):
            print(f"[ERROR] No se encontraron imágenes para el usuario con ID {id_usuario}.")
            return

        image_paths = [os.path.join(user_folder, img) for img in os.listdir(user_folder) if img.endswith('.jpg')]

        for image_path in image_paths:
            # Procesar cada imagen para obtener los encodings
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                self.known_encodings.append(encoding)
                self.known_ids.append(id_usuario)  # Asociar encoding con el ID
                self.known_names.append(nombre)  # Asociar encoding con el nombre

        # Guardar los datos actualizados
        self.guardar_encodings()
        print(f"[INFO] Entrenamiento completado para el usuario con ID {id_usuario} y nombre {nombre}.")
