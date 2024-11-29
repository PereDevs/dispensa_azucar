import os
import mysql.connector
from PIL import Image
import time
from classes.Modelo_Entrenamiento_Class import ModeloEntrenamiento
from datetime import datetime



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
                    tipo_azucar = 'blanco'
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
            while photo_count < max_photos:
                frame = picam2.capture_array()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.id_usuario}_{self.nombre}_{timestamp}.jpg"
                filepath = os.path.join(self.user_folder, filename)
                with open(filepath, "wb") as f:
                    Image.fromarray(frame).save(f, format="JPEG")
                photo_count += 1
                print(f"[INFO] Foto {photo_count} guardada en {filepath}")
                time.sleep(delay_between_photos)
        finally:
            picam2.stop()
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
        """Inicia el servicio de azucar usando los datos del usuario."""
        
        try:
            # Conectar a la base de datos para obtener el nombre del tipo de azucar
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Consulta para obtener el nombre del tipo de azucar
            query = "SELECT descripcion FROM tipo_azucar WHERE id_azucar = %s"
            cursor.execute(query, (self.tipo_azucar,))
            result = cursor.fetchone()

            # Validar si se encontró el tipo de azucar
            if result:
                nombre_tipo_azucar = result[0]
            else:
                nombre_tipo_azucar = "Desconocido"

            # Log para iniciar servicio
            print(f"[INFO] Iniciando servicio de azucar para {self.nombre}.")
            print(f"[INFO] Dispensando {self.cantidad_azucar} de {nombre_tipo_azucar} para el usuario {self.nombre}.")
            main.servir_azucar(self.id_usuario)


            self.registrar_actividad(self.id_usuario,self.db_config,self.cantidad_azucar)

            # Aviso de finalización
            print("[INFO] Proceso finalizado. El azucar ha sido servido.")
            time.sleep(5)

        except mysql.connector.Error as err:
            print(f"[ERROR] No se pudo obtener el nombre del tipo de azucar: {err}")
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar el servicio de azucar: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Volver al método main() después de completar el servicio
        from main import main  # Importar al final para evitar ciclos de importación
        main.main()

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
