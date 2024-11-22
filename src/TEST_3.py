import cv2

for i in range(0, 32):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Dispositivo abierto correctamente en /dev/video{i}")
        ret, frame = cap.read()
        if ret:
            # Guarda la imagen en un archivo
            filename = f"captura_video{i}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Imagen guardada como {filename}")
        else:
            print(f"No se pudo capturar un fotograma desde /dev/video{i}")
        cap.release()
    else:
        print(f"No se pudo abrir el dispositivo /dev/video{i}")
