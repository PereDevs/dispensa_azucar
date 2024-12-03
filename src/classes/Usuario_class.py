import os
import mysql.connector
from PIL import Image
import time
from classes.Modelo_Entrenamiento_Class import ModeloEntrenamiento
from datetime import datetime

from classes.LCD_IC2_classe import LCD_I2C
import RPi.GPIO as GPIO


class UsuarioClass:
    def __init__(self, nombre, id_usuario, db_config, dataset_path, encodings_path,tipo_azucar = None,cantidad_azucar=None):
        """
        Constructor para la clase UsuarioClass.
        """
        self.nombre = nombre.lower()
        self.id_usuario = id_usuario
        self.tipo_azucar = tipo_azucar
        self.cantidad_azucar = cantidad_azucar
        self.db_config = db_config
        self.dataset_path = dataset_path
        self.encodings_path = encodings_path
        self.user_folder = os.path.join(dataset_path, str(id_usuario))
        self.lcd = LCD_I2C()

    @classmethod
    def from_db_by_id(cls, id_usuario, db_config, dataset_path, encodings_path):
        """
        Carga un usuario desde la base de datos usando su ID.
        """
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE idusuario = %s"
            cursor.execute(query, (id_usuario,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data:
                
                # Manejar valores por defecto para tipo_azucar y cantidad_azucar
                tipo_azucar = user_data.get('default_azucar', 'blanco')  # Por defecto 'blanco'
                cantidad_azucar = user_data.get('cantidad', 1)  # Por defecto 1 cucharada

                # Asegurarse de que los valores no sean None
                if tipo_azucar is None:
                    tipo_azucar = 1
                if cantidad_azucar is None:
                    cantidad_azucar = 1
                    
                return cls(
                    nombre=user_data['nombre'],
                    id_usuario=user_data['idusuario'],
                    tipo_azucar=tipo_azucar,
                    cantidad_azucar=cantidad_azucar,
                    db_config=db_config,
                    dataset_path=dataset_path,
                    encodings_path=encodings_path
                    )
            else:
                raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")
        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo conectar a la base de datos: {err}")
            raise

    def existe_en_db(self):
        """Comprueba si el usuario ya está registrado en la base de datos."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM usuarios WHERE idusuario = %s"
            cursor.execute(query, (self.id_usuario,))
            result = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return result > 0
        except mysql.connector.Error as err:
            print(f"[ERROR] Error al comprobar en la base de datos: {err}")
            return False


    def registrar_en_db(self):
        """Registra al usuario en la base de datos y luego inicia el servicio de azucar."""
        try:
            # Conexión a la base de datos
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Obtener la fecha actual
            fecha_actual = datetime.now().date()

            # Consulta SQL para insertar el usuario
            query = "INSERT INTO usuarios (idusuario, nombre, fecha_registro, default_azucar, cantidad) VALUES (%s, %s, %s, %s, %s)"
            values = (self.id_usuario, self.nombre, fecha_actual, self.tipo_azucar, self.cantidad_azucar)
            cursor.execute(query, values)

            # Confirmar la transacción
            conn.commit()

            print(f"[INFO] Usuario {self.nombre} registrado en la base de datos.")

            # <comentario>Código modificado por ChatGPT</comentario>
            # Iniciar el servicio de azucar tras registrar
            self.iniciar_servicio_azucar()

        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo registrar en la base de datos: {err}")
        
        finally:
            # Asegurar el cierre de cursor y conexión
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def obtener_nuevo_id(db_config):
        """Obtiene el siguiente ID disponible basado en la base de datos."""
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "SELECT MAX(idusuario) FROM usuarios"
            cursor.execute(query)
            resultado = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            if resultado is None:
                return 1  # Si no hay usuarios, comienza con 1
            return resultado + 1
        except mysql.connector.Error as err:
            print(f"[ERROR] Error al obtener el siguiente ID: {err}")
            return None


    def capturar_imagenes(self, picam2, max_photos=5, delay_between_photos=2):
        """Captura imágenes del usuario."""
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
            print(f"[INFO] Carpeta creada para el usuario {self.nombre} en {self.user_folder}")

        photo_count = 0
        print(f"[INFO] Iniciando captura de imágenes para {self.nombre}.")
        try:
        
            picam2.start()
            self.lcd.clear()
            self.lcd.write("Capturando en:", line=1)
                
            while photo_count < max_photos:
                frame = picam2.capture_array()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.id_usuario}_{self.nombre}_{timestamp}.jpg"
                filepath = os.path.join(self.user_folder, filename)
                with open(filepath, "wb") as f:
                    Image.fromarray(frame).save(f, format="JPEG")
                photo_count += 1
                self.lcd.write(f"Foto {photo_count} de {max_photos}", line=1)
                print(f"[INFO] Foto {photo_count} guardada en {filepath}")
                time.sleep(delay_between_photos)
        finally:
            picam2.stop()
            self.lcd.clear()
            self.lcd.write("Captura completada.", line=1)
            print(f"[INFO] Captura completada. Total de fotos guardadas: {photo_count}.")

    def entrenar_usuario(self):
        """Entrena el modelo de reconocimiento facial para este usuario."""
        try:
            print(f"[INFO] Entrenando modelo para el usuario {self.nombre}.")
            modelo = ModeloEntrenamiento(self.dataset_path, self.encodings_path)
            modelo.entrenar_usuario(self.id_usuario,self.nombre)
            print(f"[INFO] Entrenamiento completado para el usuario {self.nombre}.")
        except Exception as e:
            print(f"[ERROR] No se pudo entrenar el modelo para {self.nombre}: {e}")
    
    def iniciar_servicio_azucar(self):
        """Inicia el servicio de azúcar usando los datos del usuario."""
        try:
            # Conectar a la base de datos para obtener el nombre del tipo de azúcar
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Consulta para obtener el nombre del tipo de azúcar
            query = "SELECT descripcion FROM tipo_azucar WHERE id_azucar = %s"
            cursor.execute(query, (self.tipo_azucar,))
            result = cursor.fetchone()

            # Validar si se encontró el tipo de azúcar
            if result:
                nombre_tipo_azucar = result[0]
            else:
                nombre_tipo_azucar = "Desconocido"

            # Log para iniciar servicio
            #print(f"[INFO] Iniciando servicio de azúcar para {self.nombre}.")
            self.lcd.clear()
            self.lcd.write(f"Dispensando {self.cantidad_azucar}", line=1)
            self.lcd.write(f"para el {self.nombre}", line=1)
            print(f"[INFO] Dispensando {self.cantidad_azucar} de {nombre_tipo_azucar} para el usuario {self.nombre}.")

            # Llamar al método interno para servir azúcar
            self.servir_azucar()

            # Registrar la actividad en la base de datos
            self.registrar_actividad(self.id_usuario, self.db_config, self.cantidad_azucar)

            # Aviso de finalización
            print("[INFO] Proceso finalizado. El azúcar ha sido servido.")
            time.sleep(5)

        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo obtener el nombre del tipo de azúcar: {err}")
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar el servicio de azúcar: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def servir_azucar(self):
        from main import PIN_MOTOR_CONTENEDOR1, PIN_MOTOR_CONTENEDOR2, PIN_MOTOR_CONTENEDOR3

        """Sirve azúcar utilizando los motores definidos en main.py."""
        # Configuración de pines
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_MOTOR_CONTENEDOR1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_CONTENEDOR2, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_CONTENEDOR3, GPIO.OUT)

        # Diccionario para mapear tipo de azúcar a los pines de los motores
        azucar_a_motor = {
            "blanco": PIN_MOTOR_CONTENEDOR1,
            "moreno": PIN_MOTOR_CONTENEDOR2,
            "edulcorante": PIN_MOTOR_CONTENEDOR3,
        }

        # Obtener el pin correspondiente al tipo de azúcar
        motor_pin = azucar_a_motor.get(self.tipo_azucar.lower())

        if not motor_pin:
            print(f"[ERROR] Tipo de azúcar desconocido: {self.tipo_azucar}")
            self.lcd.clear()
            self.lcd.write("Error: tipo azucar")
            return

        try:
            # Inicializar PWM para el motor correspondiente
            pwm_motor = GPIO.PWM(motor_pin, 50)  # Frecuencia de 50Hz
            pwm_motor.start(7.5)  # Posición inicial (0 grados)

            self.lcd.clear()
            self.lcd.write("Sirviendo azucar")
            print(f"[INFO] Sirviendo {self.cantidad_azucar} de {self.tipo_azucar} para {self.nombre}.")

            # Girar el motor para dispensar azúcar
            pwm_motor.ChangeDutyCycle(5)  # Girar a -90 grados
            time.sleep(0.5 * self.cantidad_azucar)  # Tiempo proporcional a la cantidad de azúcar

            # Volver a la posición inicial
            pwm_motor.ChangeDutyCycle(7.5)  # Volver a 0 grados
            time.sleep(0.5)

            # Detener el motor
            pwm_motor.stop()

            # Mensaje de éxito
            self.lcd.clear()
            self.lcd.write("Azucar servido")
            print("[INFO] Azúcar servido correctamente.")

        except Exception as e:
            print(f"[ERROR] Falló el servicio de azúcar: {e}")
            self.lcd.clear()
            self.lcd.write("Error serv azucar")
        finally:
            # Limpiar configuración de GPIO
            GPIO.cleanup()

    def registrar_actividad(self, id_usuario, db_config, cantidad_servicio=None):
        """
        Registra la actividad del usuario después de servir azucar.
        :param id_usuario: ID del usuario reconocido.
        :param db_config: Configuración de la base de datos.
        :param cantidad_servicio: Cantidad de azucar servida (si es None, se obtiene de la base de datos).
        """
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Si no se proporciona cantidad_servicio, obtenerla de la base de datos
            if cantidad_servicio is None:
                query_cantidad = "SELECT cantidad FROM usuarios WHERE idusuario = %s"
                cursor.execute(query_cantidad, (id_usuario,))
                result = cursor.fetchone()
                cantidad_servicio = result[0] if result else 1.0  # Valor predeterminado si no se encuentra

            # Consulta para insertar actividad
            query = """
            INSERT INTO actividad (idusuario, id_azucar, fecha_servicio, cantidad_servicio)
            VALUES (%s, 
                    (SELECT default_azucar FROM usuarios WHERE idusuario = %s), 
                    NOW(), 
                    %s)
            """
            cursor.execute(query, (id_usuario, id_usuario, cantidad_servicio))
            conn.commit()
            print(f"[INFO] Actividad registrada para el usuario con ID: {id_usuario} y cantidad: {cantidad_servicio}")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo registrar la actividad: {err}")
