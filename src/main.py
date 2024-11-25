from gpiozero import Button
from classes.LCD_IC2_classe import LCD_I2C
import os
from picamera2 import Picamera2
from classes.Usuario_class import UsuarioClass
from classes.Reconocimiento_class import Reconocimiento
import time

# Configuración
DB_CONFIG = {
    'user': 'sugar',
    'password': '12345',
    'host': 'localhost',
    'database': 'sugardb'
}
DATASET_PATH = "/home/admin/dispensa_azucar/dataset"
ENCODINGS_PATH = os.path.join(DATASET_PATH, "encodings.pickle")

# Inicialización de dispositivos
picam2 = Picamera2()
lcd = LCD_I2C()
button = Button(24)  # GPIO 17 configurado para el botón físico

def proceso_principal():
    """Flujo principal del sistema."""
    camera_active = False

    # Mensaje de inicio en el LCD
    lcd.clear()
    lcd.write("Iniciando", line=1)
    lcd.write("sistema...", line=2)

    # Inicialización de reconocimiento
    reconocimiento = Reconocimiento(ENCODINGS_PATH, DB_CONFIG)

    while True:
        try:
            # Detener la cámara si está activa
            if camera_active:
                picam2.stop()
                camera_active = False

            # Configurar y activar la cámara
            picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
            picam2.start()
            camera_active = True
            
            lcd.clear()
            lcd.write("Mira a la ", line=1)
            lcd.write("cámara...", line=2)
            time.sleep(3)

            # Capturar frame desde la cámara
            frame = picam2.capture_array()
            time.sleep(2)

            # Intentar reconocer usuario
            nombre = reconocimiento.intentar_reconocer(frame)
            time.sleep(2)
            if nombre == "Desconocido":
                lcd.clear()
                lcd.write("Usuario no", line=1)
                lcd.write("reconocido", line=2)

                # Intentar registrar nuevo usuario
                intentos = int(input("¿Intentar registro? (1 para sí, 0 para no): "))
                if intentos:
                    nombre = input("Introduce el nombre del usuario: ").strip()
                    id_usuario = UsuarioClass.obtener_nuevo_id(DB_CONFIG)
                    tipoazucar = input("Tipo de azucar (1 -Blanco 2-Moreno 3-Edulcorante): ").strip()

                    # Crear instancia de Usuario
                    nuevo_usuario = UsuarioClass(nombre, id_usuario, tipoazucar, DB_CONFIG, DATASET_PATH, ENCODINGS_PATH)

                    # Registrar en la base de datos si no existe
                    if not nuevo_usuario.existe_en_db():

                        # Capturar imágenes y entrenar modelo
                        lcd.clear()
                        lcd.write("Capturando...", line=1)
                        nuevo_usuario.capturar_imagenes(picam2)

                        lcd.clear()
                        lcd.write("Entrenando...", line=1)
                        nuevo_usuario.entrenar_usuario()

                        # Actualizar encodings en el sistema
                        reconocimiento.cargar_encodings()

                        nuevo_usuario.registrar_en_db()

                        lcd.clear()
                        lcd.write("Usuario", line=1)
                        lcd.write("registrado!", line=2)
                    else:
                        lcd.clear()
                        lcd.write("Ya existe", line=1)
                        lcd.write("en la DB", line=2)
                        time.sleep(2)  # Pausa antes de reiniciar el ciclo
            else:
                lcd.clear()
                lcd.write("Bienvenido", line=1)
                lcd.write(nombre, line=2)

                # Mostrar información básica del usuario
                reconocimiento.mostrar_informacion(lcd, nombre)

                # Simular servir azúcar
                lcd.clear()
                lcd.write("Sirviendo", line=1)
                lcd.write("azúcar...", line=2)
                lcd.clear()
                lcd.write("Proceso", line=1)
                lcd.write("completo!", line=2)
                
        except KeyboardInterrupt:
            # Mensaje de detención del sistema
            lcd.clear()
            lcd.write("Sistema", line=1)
            lcd.write("detenido", line=2)
            break
        except Exception as e:
            # Mensaje de error
            lcd.clear()
            lcd.write("Error", line=1)
            lcd.write("Revisar log", line=2)
            print(f"[ERROR] {e}")
        finally:
            # Asegurarse de que la cámara se detenga al final del ciclo
            if camera_active:
                picam2.stop()
                camera_active = False

def main():
    """Bucle principal de espera por botón."""
    lcd.clear()
    lcd.write("Pulsa botón", line=1)
    lcd.write("para azúcar", line=2)
    
    while True:
        # Espera por pulsación del botón
        button.wait_for_press()
        lcd.clear()
        lcd.write("Procesando...", line=1)
        proceso_principal()

if __name__ == "__main__":
    main()
