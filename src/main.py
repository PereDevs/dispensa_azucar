from classes.LCD_IC2_classe import LCD_I2C

lcd = LCD_I2C()
lcd.clear() 
lcd.write("Cargando", line=1)
lcd.write("Espera...", line=2)

import os
from gpiozero import Button
from picamera2 import Picamera2
from classes.Usuario_class import UsuarioClass
from classes.Reconocimiento_class import Reconocimiento
from classes.taza_class import Taza
from classes.Contenedor_Class import Contenedor
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
PIN_SENSOR_TAZA = 24
PIN_BOTON = 18
button = Button(PIN_BOTON)

# Pines de los motores para cada contenedor
PIN_MOTOR_CONTENEDOR1 = 21  # Azucar blanco
PIN_MOTOR_CONTENEDOR2 = 12  # Azucar moreno
PIN_MOTOR_CONTENEDOR3 = 26  # Edulcorante

# Crear instancias de contenedores
contenedor_blanco = Contenedor(capacidad_total=100, motor_pin=PIN_MOTOR_CONTENEDOR1, boton_pin=PIN_BOTON, lcd=lcd, db_config = DB_CONFIG,tipo_azucar=1)
contenedor_moreno = Contenedor(capacidad_total=100, motor_pin=PIN_MOTOR_CONTENEDOR2, boton_pin=PIN_BOTON, lcd=lcd,db_config = DB_CONFIG,tipo_azucar=2)
contenedor_edulcorante = Contenedor(capacidad_total=100, motor_pin=PIN_MOTOR_CONTENEDOR3, boton_pin=PIN_BOTON, lcd=lcd,db_config = DB_CONFIG,tipo_azucar=3)

# Inicialización de dispositivos
try:
    picam2 = Picamera2()
    taza = Taza(pin_sensor=PIN_SENSOR_TAZA)
    camera_active = False
except Exception as e:
    print(f"[ERROR] Problema con la inicialización de la cámara o el botón: {e}")
    exit(1)

def servir_azucar(usuario):
    """
    Sirve azucar según las preferencias del usuario.
    """
    tipo_azucar = usuario.tipo_azucar  # 1: Blanco, 2: Moreno, 3: Edulcorante
    cantidad = usuario.cantidad_azucar  # Cantidad en gramos

    if tipo_azucar == 1:
        resultado = contenedor_blanco.dispensar_azucar(cantidad)
    elif tipo_azucar == 2:
        resultado = contenedor_moreno.dispensar_azucar(cantidad)
    elif tipo_azucar == 3:
        resultado = contenedor_edulcorante.dispensar_azucar(cantidad)
    else:
        lcd.clear()
        lcd.write("Error: Tipo", line=1)
        lcd.write("de azucar", line=2)
        return "Error: Tipo de azucar no válido"

    if "Error" in resultado:
        lcd.clear()
        lcd.write("Error con el", line=1)
        lcd.write("contenedor", line=2)
        time.sleep(5)
    else:
        lcd.clear()
        lcd.write("Azucar listo!", line=1)
        time.sleep(3)

    return resultado

def detener_camara():
    """Detiene la cámara si está activa."""
    global camera_active
    if camera_active:
        picam2.stop()
        camera_active = False
        print("[INFO] Cámara detenida.")  # Log de depuración

def proceso_principal():
    """Flujo principal del sistema."""
    global camera_active

    try:
        # Verificar si la taza está presente antes de iniciar el proceso principal
        lcd.clear()
        lcd.write("Verificando", line=1)
        lcd.write("taza...", line=2)
        while not taza.taza_presente():
            lcd.clear()
            lcd.write("Pon la taza", line=1)
            time.sleep(1)

        lcd.clear()
        lcd.write("Taza lista", line=1)
        time.sleep(2)

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
        reconocimiento = Reconocimiento(ENCODINGS_PATH, DB_CONFIG)
        id_usuario = reconocimiento.intentar_reconocer(frame)
        time.sleep(1)

        if id_usuario == "Desconocido":
            while id_usuario == "Desconocido":  # 28 Nov: Bucle para reintentar reconocimiento
                lcd.clear()
                lcd.write("Usuario no", line=1)
                lcd.write("reconocido", line=2)

                intentos = int(input("¿Intentar registro? (1 para sí, 0 para no): "))
                if intentos == 1:
                    # Registro de nuevo usuario
                    nombre = input("Introduce el nombre del usuario: ").strip()
                    id_usuario = UsuarioClass.obtener_nuevo_id(DB_CONFIG)
                    tipoazucar = input("Tipo de azucar (1 -Blanco 2-Moreno 3-Edulcorante): ").strip()
                    cantidadazucar = input("Cuántas cucharadas de azucar? ").strip()
                    cantidadazucar_int = 4 * int(cantidadazucar)

                    nuevo_usuario = UsuarioClass(
                        nombre, id_usuario, DB_CONFIG, DATASET_PATH, ENCODINGS_PATH, tipoazucar, cantidadazucar_int
                    )
                    if not nuevo_usuario.existe_en_db():
                        for i in range(5, 0, -1):
                            lcd.clear()
                            lcd.write("Capturando en:", line=1)
                            lcd.write(f"{i}...mira a camara", line=2)
                            time.sleep(1)

                        lcd.clear()
                        lcd.write("Capturando...", line=1)
                        time.sleep(2)
                        nuevo_usuario.capturar_imagenes(picam2)

                        lcd.clear()
                        lcd.write("Entrenando...", line=1)
                        time.sleep(2)
                        nuevo_usuario.entrenar_usuario()
                        reconocimiento.cargar_encodings()

                        nuevo_usuario.registrar_en_db()

                elif intentos == 0:
                    # Reintentar reconocimiento
                    lcd.clear()
                    lcd.write("Intentando", line=1)
                    lcd.write("reconocer...", line=2)
                    time.sleep(3)

                    frame = picam2.capture_array()
                    id_usuario = reconocimiento.intentar_reconocer(frame)

            # Cuando se reconoce el usuario, continuar el flujo
            lcd.clear()
            lcd.write("Bienvenido", line=1)
            usuario = UsuarioClass.from_db_by_id(
                id_usuario=id_usuario,
                db_config=DB_CONFIG,
                dataset_path=DATASET_PATH,
                encodings_path=ENCODINGS_PATH
            )
            lcd.write(f"{usuario.nombre}", line=2)
            time.sleep(2)

            resultado = servir_azucar(usuario)
            print(f"[INFO] Resultado del servicio: {resultado}")

            # Mostrar información del usuario en la LCD
            reconocimiento.mostrar_informacion(lcd, id_usuario)  # Llamada añadida

            lcd.clear()
            lcd.write("Proceso completo!", line=1)
            lcd.write("Retira tu taza", line=2)
            time.sleep(3)


    except KeyboardInterrupt:
        lcd.clear()
        lcd.write("Sistema", line=1)
        lcd.write("detenido", line=2)
        time.sleep(5)
        lcd.clear()
        exit(0)
    except Exception as e:
        lcd.clear()
        lcd.write("Error", line=1)
        lcd.write("Revisar log", line=2)
        print(f"[ERROR] {e}")
        time.sleep(5)
        lcd.clear()
    finally:
        detener_camara()  # Detener la cámara siempre al finalizar
        print("[INFO] Retornando al estado de espera del botón.")  # Log de depuración
        main()

def main():
    """Bucle principal de espera por botón."""
    lcd.clear()
    lcd.write("Pulsa boton", line=1)
    lcd.write("para azucar", line=2)

    while True:
        # Espera por pulsación del botón
        detener_camara()
        button.wait_for_press()
        lcd.clear()
        lcd.write("Procesando...", line=1)
        time.sleep(2)
        proceso_principal()  # Volver al proceso principal

if __name__ == "__main__":
    main()
