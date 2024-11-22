import os
import cv2
import face_recognition
import sqlite3
import pickle
import time

class FaceRecognitionClass:
    def __init__(self, db_path, encodings_path):
        """
        Clase para manejar el reconocimiento facial.
        :param db_path: Ruta a la base de datos SQLite.
        :param encodings_path: Ruta al archivo pickle con los encodings.
        """
        self.db_path = db_path
        self.encodings_path = encodings_path

        # Cargar encodings si existen
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, "rb") as f:
                self.data = pickle.load(f)
        else:
            self.data = {"ids": [], "encodings": []}
            print("[INFO] No se encontraron encodings. El archivo se creará con el primer registro.")

    def reconocer_usuario(self, timeout=5):
        """
        Detecta rostros y compara con los encodings almacenados.
        Si no se detecta ningún rostro en el tiempo especificado, sigue adelante.
        :param timeout: Tiempo máximo en segundos para intentar detectar un rostro.
        :return: ID del usuario reconocido o None si no se reconoce.
        """
        start_time = time.time()
        print("[INFO] Intentando detectar rostro...")

        while time.time() - start_time < timeout:
            # Capturar un cuadro de la cámara
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            if not ret:
                print("[ERROR] No se pudo capturar la imagen.")
                camera.release()
                return None

            # Procesar el cuadro
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            camera.release()

            if len(face_locations) > 0:
                # Si detectamos un rostro, procesamos el encoding
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                matches = face_recognition.compare_faces(self.data["encodings"], face_encoding)

                if True in matches:
                    matched_idx = matches.index(True)
                    user_id = self.data["ids"][matched_idx]
                    return user_id

                print("[INFO] Usuario desconocido.")
                return None

            # Espera un corto tiempo antes de capturar de nuevo
            time.sleep(0.5)

        print("[INFO] Tiempo agotado: No se detectaron rostros.")
        return None

    def get_user_data(self, user_id):
        """
        Obtiene los datos del usuario desde la base de datos.
        :param user_id: ID del usuario.
        :return: Diccionario con los datos del usuario.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT idusuario, nombre, apellidos, default_azucar
            FROM usuarios
            WHERE idusuario = ?
        """, (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {"idusuario": user[0], "nombre": user[1], "apellidos": user[2], "default_azucar": user[3]}
        return None
