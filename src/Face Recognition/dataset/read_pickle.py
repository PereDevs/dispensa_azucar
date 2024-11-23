import pickle

encodings_path = "/home/admin/dispensa_azucar/src/Face Recognition/dataset/encodings.pickle"

with open(encodings_path, "rb") as f:
    data = pickle.load(f)

# Imprime los nombres y encodings para inspección
for entry in data:
    print(f"Nombre: {entry['name']}, ID: {entry['id']}, Encoding: {entry['encoding'][:5]}...")