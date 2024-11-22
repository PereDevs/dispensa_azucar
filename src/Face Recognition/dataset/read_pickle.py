import pickle

# Cargar las codificaciones desde el archivo
with open('/home/admin/dispensa_azucar/src/Face Recognition/dataset/encodings.pickle', 'rb') as f:
    data = pickle.load(f)

# Extraer los nombres de los usuarios
known_names = data.get("names", [])

print(known_names)