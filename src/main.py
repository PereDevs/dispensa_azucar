import os
import sys
from picamera2 import Picamera2
from classes.Usuario_class import Usuario
from classes.reconocimiento_class import Reconocimiento
from classes.Modelo_Entrenamiento_Class import ModeloEntrenamiento
from classes.LCD_IC2_classe import LCD

# Configuración
DB_CONFIG = {
    'user': 'sugar',
    'password': 'sugar',
    'host': 'localhost',
    'database': 'sugardb'
}
DATASET_PATH = "/home/admin/dispensa_azucar/src/Face Recognition/dataset"
ENCODINGS_PATH = os.path.join(DATASET_PATH, "encodings.pickle")

# Inicialización de dispositivos
picam2 = Picamera2()
lcd = LCD()

def main():
    """Flujo principal del sistema."""
    # print("[INFO] Iniciando sistema...")
    lcd.clear()
    lcd.write("Iniciando", line=1)
    lcd.write("sistema...", line=2)
    
    reconocimiento = Reconocimiento(ENCODINGS_PATH, DB_CONFIG)
    modelo = ModeloEntrenamiento(DATASET_PATH, ENCODINGS_PATH)

    while True:
        try:
            # Capturar frame desde la cámara
            frame = picam2.capture_array()
            
            # Intentar reconocer usuario
            nombre = reconocimiento.intentar_reconocer(frame)
            if nombre == "Desconocido":
                # print("[INFO] Usuario desconocido.")
                lcd.clear()
                lcd.write("Usuario no", line=1)
                lcd.write("reconocido", line=2)

                # Intentar registrar nuevo usuario
                intentos = int(input("¿Intentar registro? (1 para sí, 0 para no): "))
                if intentos:
                    nombre = input("Introduce el nombre del usuario: ").strip()
                    id_usuario = input("Introduce el ID del usuario: ").strip()

                    # Crear instancia de Usuario
                    nuevo_usuario = Usuario(nombre, id_usuario, DB_CONFIG, DATASET_PATH, ENCODINGS_PATH)

                    # Registrar en DB si no existe
                    if not nuevo_usuario.existe_en_db():
                        nuevo_usuario.registrar_en_db()

                        # Capturar imágenes y entrenar modelo
                        lcd.clear()
                        lcd.write("Capturando...", line=1)
                        nuevo_usuario.capturar_imagenes(picam2)
                        
                        lcd.clear()
                        lcd.write("Entrenando...", line=1)
                        nuevo_usuario.entrenar_usuario()

                        lcd.clear()
                        lcd.write("Usuario", line=1)
                        lcd.write("registrado!", line=2)
                        # print("[INFO] Usuario registrado exitosamente.")
            else:
                # print(f"[INFO] Usuario reconocido: {nombre}")
                lcd.clear()
                lcd.write("Bienvenido", line=1)
                lcd.write(nombre, line=2)

                # Mostrar información básica del usuario
                reconocimiento.mostrar_informacion(lcd, nombre)

                # Simular servir azúcar
                # print("[INFO] Sirviendo azúcar...")
                lcd.clear()
                lcd.write("Sirviendo", line=1)
                lcd.write("azúcar...", line=2)
                # Aquí se incluiría la lógica para servir azúcar
                # print("[INFO] Azúcar servido.")
                lcd.clear()
                lcd.write("Proceso", line=1)
                lcd.write("completo!", line=2)

        except KeyboardInterrupt:
            # print("\n[INFO] Sistema detenido por el usuario.")
            lcd.clear()
            lcd.write("Sistema", line=1)
            lcd.write("detenido", line=2)
            break
        except Exception as e:
            # print(f"[ERROR] Ocurrió un error inesperado: {e}")
            lcd.clear()
            lcd.write("Error", line=1)
            lcd.write("Revisar log", line=2)

if __name__ == "__main__":
    main()
