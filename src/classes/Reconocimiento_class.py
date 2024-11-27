import face_recognition
import cv2
from classes.LCD_IC2_classe import LCD_I2C

import numpy as np
import pickle
import os
import mysql.connector  # Cambiado 'mysql' a 'mysql.connector' para evitar confusiones
import time

class Reconocimiento:
    def __init__(self, encodings_path, db_config):
        self.encodings_path = encodings_path
        self.db_config = db_config
        self.known_face_encodings = []  # Inicializar lista para encodings
        self.known_ids = []  # Inicializar lista para IDs
        self.known_names = []  # Inicializar lista para nombres
        self.cargar_encodings()  # Cargar encodings al inicializar

    def cargar_encodings(self):  # Modificado por CHATGPT 26/11/2024 15:10
        """Carga los encodings desde el archivo."""
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, "rb") as f:
                data = pickle.load(f)
                # Asignar datos cargados a las listas correspondientes
                self.known_face_encodings = data.get("encodings", [])
                self.known_ids = data.get("ids", [])  # Cargar IDs por separado
                self.known_names = data.get("names", [])  # Cargar nombres por separado
        else:
            print("[INFO] No se encontró archivo de encodings. Inicializando vacío.")
            self.known_face_encodings = []  # Inicializar lista vacía para encodings
            self.known_ids = []  # Inicializar lista vacía para IDs
            self.known_names = []  # Inicializar lista vacía para nombres

    def intentar_reconocer(self, frame):
        """
        Intenta reconocer una cara en un frame capturado.
        :param frame: Frame capturado por la cámara.
        :return: ID del usuario reconocido o "Desconocido".
        """
        try:
            # Reducir resolución del frame para mejorar rendimiento
            cv_scaler = 4  # Escalar a 1/4 del tamaño original
            resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))

            # Convertir el frame a RGB
            rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

            # Detectar ubicaciones y codificaciones faciales
            face_locations = face_recognition.face_locations(rgb_resized_frame, model='hog')
            face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

            # Procesar cada codificación de rostro encontrada
            for face_encoding in face_encodings:
                # Comparar con las codificaciones conocidas
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"

                # Calcular distancias y encontrar la mejor coincidencia
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                if matches:  # Verificar si hay coincidencias
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]  # Obtener el nombre del usuario reconocido
                        id_usuario = self.known_ids[best_match_index]  # Obtener el ID correspondiente
                        lcd = LCD_I2C()
                        lcd.clear()
                        print(f"[INFO] Usuario reconocido: {name} (ID: {id_usuario})")
                        return id_usuario

            # Si no hay coincidencias, retornar "Desconocido"
            print("[INFO] Usuario desconocido.")
            return "Desconocido"


        except Exception as e:
            print(f"[ERROR] Problema durante el reconocimiento facial: {e}")
            return "Desconocido"

    def mostrar_informacion(self, lcd, idusuario):  # Modificado por CHATGPT 26/11/2024 15:30
        """Muestra la información del usuario en el LCD."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            # Consulta corregida para obtener el campo 'nombre'
            query = """
            SELECT 
                usuarios.nombre,
                tipo_azucar.descripcion AS tipo_azucar,
                SUM(actividad.cantidad_servicio) AS cantidad_consumida
            FROM 
                usuarios
            LEFT JOIN 
                actividad ON usuarios.idusuario = actividad.idusuario
            LEFT JOIN 
                tipo_azucar ON usuarios.default_azucar = tipo_azucar.id_azucar
            WHERE 
                usuarios.idusuario = %s 
                AND actividad.fecha_servicio >= NOW() - INTERVAL 30 DAY
            GROUP BY 
                usuarios.idusuario
            """
            cursor.execute(query, (idusuario,))
            user_info = cursor.fetchone()
            
            # Validar si se encontró información del usuario
            lcd = LCD_I2C()
            
            if user_info:
                lcd.clear()
                #lcd.write(f"Bienvenido, {user_info['nombre']}", line=1)  # Cambiado de 'nombreclear' a 'nombre'
                time.sleep(2)
                tipo_azucar = user_info.get('tipo_azucar', 'N/A')
                cantidad_consumida = user_info.get('cantidad_consumida', 0)
                lcd.clear()
                lcd.write(f" {user_info['nombre']}, te muestro", line=1)  # Cambiado de 'nombreclear' a 'nombre'
                lcd.write("consumo 30 dias", line=2)  # Cambiado de 'nombreclear' a 'nombre'
                time.sleep(5)
                lcd.clear()
                lcd.write(f"Tipo: {tipo_azucar}", line=1)  # Cambiado de 'nombreclear' a 'nombre'
                lcd.write(f"Consumo: {cantidad_consumida}", line=2)
                time.sleep(5)
                
            else:
                lcd.clear()
                lcd.write("Usuario no", line=1)
                lcd.write("encontrado", line=2)

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo obtener información del usuario: {err}")
