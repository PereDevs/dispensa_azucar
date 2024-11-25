import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import pickle
import os
import mysql
import time

class Reconocimiento:
    def __init__(self, encodings_path, db_config):
        self.encodings_path = encodings_path
        self.db_config = db_config
        self.known_face_encodings = []
        self.known_face_names = []
        self.cargar_encodings()
    
    def cargar_encodings(self):
        """Carga los encodings desde el archivo o inicializa si no existe."""
        try:
            if os.path.exists(self.encodings_path):
                with open(self.encodings_path, "rb") as f:
                    data = pickle.load(f)
                    if isinstance(data, dict):  # Validar que sea un diccionario
                        self.known_face_encodings = data.get("encodings", [])
                        self.known_face_names = data.get("names", [])
                        print("[INFO] Encodings cargados correctamente.")
                    else:
                        print("[ERROR] El archivo de encodings no tiene el formato esperado. Inicializando vacío.")
                        self.known_face_encodings = []
                        self.known_face_names = []
            else:
                print("[INFO] Archivo de encodings no encontrado. Inicializando vacío.")
                self.known_face_encodings = []
                self.known_face_names = []
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar los encodings: {e}")
            self.known_face_encodings = []
            self.known_face_names = []


    def intentar_reconocer(self, frame):
        """Intenta reconocer una cara en un frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            time.sleep(2)
            name = "Desconocido"
            if True in matches:
                best_match_index = np.argmin(face_recognition.face_distance(self.known_face_encodings, face_encoding))
                name = self.known_face_names[best_match_index]
            return name
        return "Desconocido"

    def mostrar_informacion(self, lcd, nombre):
        """Muestra la información del usuario en el LCD."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT nombreclear 
            FROM usuarios 
            WHERE nombre = %s
            """
            cursor.execute(query, (nombre,))
            user_info = cursor.fetchone()
            if user_info:
                lcd.clear()
                lcd.write(f"{user_info['nombre']}", line=1)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo obtener información del usuario: {err}")