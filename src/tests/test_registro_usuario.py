
from picamera2 import Picamera2
from Usuario_registro_class import *

# Configuración de conexión a MariaDB
db_config = {
    "host": "localhost",        # Cambia esto a la IP/host de tu servidor MariaDB
    "user": "sugar",       # Usuario de la base de datos
    "password": "12345", # Contraseña de la base de datos
    "database": "sugardb"   # Nombre de la base de datos
}

encodings_path = "encodings.pickle"

# Crear una instancia de UsuarioRegistro
registro = UsuarioRegistro(db_config, encodings_path)
print(f"Ruta de encodings_path: {os.path.abspath(encodings_path)}")


try:
    # Registrar un usuario nuevo
    registro.registrar_usuario("Juan", "Pérez", 1)

except Exception as e:
    print(f"[ERROR] {str(e)}")

finally:
    # Detener la cámara
    registro.detener_camara()
