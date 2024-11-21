import cv2
import os
from datetime import datetime
from picamera2 import Picamera2
import time


import os
import time
import cv2
from datetime import datetime
from picamera2 import Picamera2

class Capture():
    def __init__(self):
        pass

    def create_folder(self, name):
        """
        Crea una carpeta para almacenar las fotos del usuario.
        """
        dataset_folder = "dataset"
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)
        
        person_folder = os.path.join(dataset_folder, name)
        if not os.path.exists(person_folder):
            os.makedirs(person_folder)
        
        return person_folder

    def capture_photos(self, name):
        """
        Captura fotos del usuario y las guarda en la carpeta correspondiente.
        """
        folder = self.create_folder(name)
        
        # Inicializar la cámara
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        picam2.start()

        # Esperar que la cámara se caliente
        time.sleep(2)

        photo_count = 0
        print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
        
        while True:
            # Capturar un fotograma
            frame = picam2.capture_array()
            
            # Mostrar el fotograma en una ventana
            #cv2.imshow('Capture', frame)
            print("Capture")
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Tecla espacio
                photo_count += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}.jpg"
                filepath = os.path.join(folder, filename)
                cv2.imwrite(filepath, frame)
                print(f"Photo {photo_count} saved: {filepath}")
            
            elif key == ord('q'):  # Tecla 'q'
                break
        
        # Limpiar recursos
        cv2.destroyAllWindows()
        picam2.stop()
        print(f"Photo capture completed. {photo_count} photos saved for {name}.")
