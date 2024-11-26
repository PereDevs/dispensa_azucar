import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
from RPLCD.i2c import CharLCD  # Biblioteca para manejar el LCD I2C

# Configuración del LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)
lcd.clear()

# Cargar codificaciones de rostros preentrenadas
print("[INFO] Cargando codificaciones...")
with open("/home/admin/dispensa_azucar/dataset/encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Inicializar la cámara
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

# Variables iniciales
cv_scaler = 4  # Reducir resolución para mayor rendimiento
face_locations = []
face_encodings = []
face_names = []

try:
    while True:
        # Capturar un frame de la cámara
        frame = picam2.capture_array()
        
        # Reducir la resolución del frame para un procesamiento más rápido
        resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))
        
        # Convertir el frame a RGB
        rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        
        # Localizar rostros y obtener codificaciones en el frame
        face_locations = face_recognition.face_locations(rgb_resized_frame)
        face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
        
        # Procesar cada rostro encontrado en el frame
        for face_encoding in face_encodings:
            # Comparar con rostros conocidos
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Usuario desconocido"
            
            # Verificar la coincidencia más cercana
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            # Imprimir el nombre en la consola
            print(f"[INFO] {name}")
            
            # Enviar el mensaje al LCD
            lcd.clear()
            if name == "Usuario desconocido":
                lcd.write_string("ERES DESCONOCIDO")
            else:
                lcd.write_string(f"ERES {name}")
        
        # Si no se detectan rostros, mostrar un mensaje predeterminado en el LCD
        if not face_encodings:
            print("[INFO] No se detectaron rostros.")
            lcd.clear()
            lcd.write_string("NO SE DETECTAN\nROSTROS")
        
        # Espera opcional para estabilidad
        time.sleep(1)

except KeyboardInterrupt:
    # Manejar la interrupción manual (Ctrl+C) y liberar recursos
    print("\n[INFO] Proceso detenido por el usuario.")
finally:
    # Asegurarse de limpiar el LCD y detener la cámara
    lcd.clear()
    lcd.write_string("Sistema detenido")
    time.sleep(2)
    lcd.clear()
    picam2.stop()
