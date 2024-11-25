import cv2
from picamera2 import Picamera2
import time
import numpy as np
import matplotlib.pyplot as plt



    

# Cargar el clasificador preentrenado para detección de rostros
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('/home/admin/py_projects/facial-recognition-main/haarcascade_frontalface_default.xml')


# Inicializar Picamera2
picam2 = Picamera2()

# Configurar la resolución y el formato de la cámara
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)

try:
    if picam2:
        print("Deteniendo la cámara...")
        picam2.stop()
        print("Cámara detenida.")
except Exception as e:
    print(f"Error al detener la cámara: {e}")
    
# Iniciar la cámara
picam2.start()
print("Camara iniciada")
# Permitir que la cámara se estabilice
time.sleep(2)

# Cargar la imagen de referencia del rostro
face_reference = cv2.imread('/home/admin/dispensa_azucar/src/pere_7.jpg', cv2.IMREAD_GRAYSCALE)

# Capturar y procesar frames en tiempo real
while True:
    # Capturar un frame como un array de NumPy
    frame = picam2.capture_array()
    
    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros en el frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Comparar el rostro detectado con la imagen de referencia
        detected_face = gray[y:y+h, x:x+w]
        detected_face_resized = cv2.resize(detected_face, (face_reference.shape[1], face_reference.shape[0]))
        similarity_score = cv2.matchTemplate(detected_face_resized, face_reference, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(similarity_score)
        
        if max_val >= 0.8:  # Ajustar este umbral según sea necesario
            cv2.putText(frame, "Your Name", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Mostrar el frame resultante
    
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    #cv2.imshow("Face Recognition", frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Detener la cámara y cerrar todas las ventanas
picam2.stop()
cv2.destroyAllWindows()
