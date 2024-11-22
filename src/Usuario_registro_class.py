import sqlite3
import face_recognition
import pickle
import os
from picamera2 import Picamera2
import mysql.connector


class UsuarioRegistro:
    def __init__(self, db_path, encodings_path):
        """
        Clase para registrar usuarios y manejar encodings.
        :param db_path: Ruta a la base de datos SQLite.
        :param encodings_path: Ruta al archivo pickle para guardar los encodings.
        """
        self.db_path = db_path
        self.encodings_path = encodings_path
        self.picam2 = Picamera2()  # Inicializar Picamera2
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
        self.picam2.start()

    def _connect_db(self):
        """
        Establece una conexión a la base de datos MariaDB.
        :return: Conexión activa a la base de datos.
        """
        return mysql.connector.connect(**self.db_config)

    def registrar_usuario(self, nombre, apellidos, default_azucar):
        """
        Registra un nuevo usuario en la base de datos y guarda su encoding.
        :param nombre: Nombre del usuario.
        :param apellidos: Apellidos del usuario.
        :param default_azucar: Tipo de azúcar preferido.
        """
        print("[INFO] Capturando rostro...")

        # Capturar un cuadro desde la cámara
        frame = self.picam2.capture_array()

        # Detectar el rostro y calcular su encoding
        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) == 0:
            print("[ERROR] No se detectaron rostros.")
            return

        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

        # Insertar el usuario en la base de datos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellidos, default_azucar)
            VALUES (?, ?, ?)
        """, (nombre, apellidos, default_azucar))
        user_id = cursor.lastrowid  # Obtener el ID asignado al usuario
        conn.commit()
        conn.close()
        print(f"[INFO] Usuario registrado con ID: {user_id}")

        # Guardar el encoding en el archivo pickle
        self._guardar_encoding(user_id, face_encoding)

    def _guardar_encoding(self, user_id, face_encoding):
        """
        Guarda el encoding del usuario en el archivo pickle.
        :param user_id: ID del usuario en la base de datos.
        :param face_encoding: Encoding facial del usuario.
        """
        if os.path.exists(self.encodings_path):
            # Cargar encodings existentes
            with open(self.encodings_path, "rb") as f:
                data = pickle.load(f)
        else:
            # Crear estructura inicial si no existe el archivo
            data = {"ids": [], "encodings": []}

        # Agregar el nuevo encoding y ID
        data["ids"].append(user_id)
        data["encodings"].append(face_encoding)

        # Guardar los datos actualizados
        with open(self.encodings_path, "wb") as f:
            pickle.dump(data, f)

        print(f"[INFO] Encoding guardado para ID: {user_id}")

    def detener_camara(self):
        """
        Detiene la cámara Picamera2.
        """
        self.picam2.stop()
        print("[INFO] Cámara detenida.")
