from Usuario_registro_class import *
from FaceRecognition_Class import *



db_path = "usuarios.db"
encodings_path = "/home/admin/dispensa_azucar/src/Face Recognition/dataset/encodings.pickle"

registro = UsuarioRegistro(db_path, encodings_path)
reconocimiento = FaceRecognitionClass(db_path, encodings_path)

# Registrar un usuario
registro.registrar_usuario("Juan", "Pérez", 1)

# Reconocer un usuario
user_id = reconocimiento.reconocer_usuario()
if user_id:
    user_data = reconocimiento.get_user_data(user_id)
    print(f"Usuario reconocido: {user_data['nombre']} {user_data['apellidos']} (Azúcar: {user_data['default_azucar']})")
else:
    print("Usuario no reconocido.")
