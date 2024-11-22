import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import os

# Load pre-trained face encodings
print("[INFO] Cargando codificaciones...")
with open("/home/admin/dispensa_azucar/src/Face Recognition/dataset/encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

# Initialize variables
cv_scaler = 8  # Reducir resolución para mayor rendimiento
face_locations = []
face_encodings = []
face_names = []

while True:
    try:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        
        # Resize the frame for faster face recognition processing
        resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))
        
        # Convert the image to RGB
        rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_resized_frame)
        face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
        
        # Process each face found in the frame
        for face_encoding in face_encodings:
            # Compare the face with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Usuario desconocido"
            
            # Use the known face with the smallest distance if there's a match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            # Print the recognized name or "Usuario desconocido"
            print(f"[INFO] {name}")
        
        # If no faces are detected, print a default message
        if not face_encodings:
            print("[INFO] No se detectaron rostros.")
        
        # Optional delay for stability (e.g., 1 frame per second)
        time.sleep(1)
    
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C to stop the process
        print("\n[INFO] Proceso detenido por el usuario.")
        break

# Release resources
picam2.stop()
