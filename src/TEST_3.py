import cv2

cap = cv2.VideoCapture(0)  # Usa el índice 0 para acceder a /dev/video0
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
else:
    print("Cámara abierta correctamente.")
    ret, frame = cap.read()
    if ret:
        print("Captura exitosa.")
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
    else:
        print("No se pudo capturar un fotograma.")

cap.release()
cv2.destroyAllWindows()

