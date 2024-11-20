from picamera2 import Picamera2
from time import sleep

def capture_images(username):
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    
    
    for i in range(10):
        image_path = f"{username}_{i+1}.jpg"
        picam2.capture_file(image_path)
        print(f"Imagen capturada: {image_path}")
        sleep(2)  # Espera 1 segundo entre cada captura (puedes ajustar)

    picam2.stop()
    print("Captura de imágenes completada.")

if __name__ == "__main__":
    capture_images("pere")