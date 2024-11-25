import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import pickle
import time


# Cargar codificaciones conocidas
print("[INFO] Cargando codificaciones...")
with open("/home/admin/dispensa_azucar/dataset/encodings.pickle", "rb") as f:
    data = pickle.load(f)

known_face_encodings = [entry["encoding"] for entry in data]
known_face_names = [entry["name"] for entry in data]

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

while True:
    try:
        frame = picam2.capture_array()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Usuario desconocido"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            print(f"[INFO] Reconocido: {name}")

        if not face_encodings:
            print("[INFO] No se detectaron rostros.")
        time.sleep(1)

    except KeyboardInterrupt:
        print("[INFO] Proceso detenido por el usuario.")
        break

picam2.stop()