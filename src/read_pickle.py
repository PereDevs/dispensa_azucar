import pickle

# Ruta del archivo pickle
archivo_pickle = "/home/admin/dispensa_azucar/dataset/encodings.pickle"

try:
    with open(archivo_pickle, "rb") as f:
        datos = pickle.load(f)  # Carga los datos desde el archivo pickle
        print("[INFO] Datos cargados correctamente:")
        print(datos)
except FileNotFoundError:
    print(f"[ERROR] El archivo {archivo_pickle} no fue encontrado.")
except pickle.UnpicklingError:
    print("[ERROR] No se pudo cargar el archivo pickle. Verifica que esté correctamente formateado.")
