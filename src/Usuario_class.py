import os
import mysql.connector
from datetime import datetime
from model_training import procesar_persona

class Usuario:
    def __init__(self, nombre, id_usuario, db_config, dataset_path):
        self.nombre = nombre.lower()
        self.id_usuario = id_usuario
        self.dataset_path = dataset_path
        self.user_folder = os.path.join(dataset_path, str(id_usuario))
        self.db_config = db_config

    def existe_en_db(self):
        """Comprueba si el usuario ya está registrado en la base de datos."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM usuarios WHERE id = %s"
            cursor.execute(query, (self.id_usuario,))
            result = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return result > 0
        except mysql.connector.Error as err:
            print(f"[ERROR] Error al comprobar en la base de datos: {err}")
            return False

    def registrar_en_db(self):
        """Registra al usuario en la base de datos."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (id, nombre) VALUES (%s, %s)"
            cursor.execute(query, (self.id_usuario, self.nombre))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"[INFO] Usuario {self.nombre} registrado en la base de datos.")
        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo registrar en la base de datos: {err}")

    def capturar_imagenes(self, picam2, max_photos=5, delay_between_photos=2):
        """Captura imágenes del usuario."""
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
            print(f"[INFO] Carpeta creada para el usuario {self.nombre} en {self.user_folder}")
        
        photo_count = 0
        print(f"[INFO] Iniciando captura de imágenes para {self.nombre}.")
        
        try:
            picam2.start()
            while photo_count < max_photos:
                frame = picam2.capture_array()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.id_usuario}_{self.nombre}_{timestamp}.jpg"
                filepath = os.path.join(self.user_folder, filename)
                with open(filepath, "wb") as f:
                    Image.fromarray(frame).save(f, format="JPEG")
                photo_count += 1
                print(f"[INFO] Foto {photo_count} guardada en {filepath}")
                time.sleep(delay_between_photos)
        finally:
            picam2.stop()
            print(f"[INFO] Captura completada. Total de fotos guardadas: {photo_count}.")

    def entrenar_usuario(self):
        """Entrena el modelo para el usuario."""
        procesar_persona(self.nombre, self.id_usuario, path=self.dataset_path)