import face_recognition
import cv2
import numpy as np

def main():
    # Carga una imagen de tu rostro conocida
    known_image = face_recognition.load_image_file("./pere_7.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]

    # Inicializa la cámara
    video_capture = cv2.VideoCapture(0)  # Usa la cámara conectada

    # Configuración de nombres
    known_face_encodings = [known_encoding]
    known_face_names = ["Eres tú"]

    print("Iniciando reconocimiento facial. Presiona 'q' para salir.")

    while True:
        # Captura un frame de la cámara
        ret, frame = video_capture.read()
        if not ret:
            print("No se pudo acceder a la cámara.")
            break

        # Convierte el frame a formato RGB para face_recognition
        rgb_frame = frame[:, :, ::-1]

        # Encuentra todas las caras en el frame y sus codificaciones
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compara la cara detectada con la cara conocida
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Desconocido"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Dibuja un rectángulo alrededor de la cara y muestra el nombre
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Muestra el frame en una ventana
        cv2.imshow("Reconocimiento Facial", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Limpia y cierra
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
