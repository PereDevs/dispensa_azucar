from gpiozero import Button
import RPi.GPIO as GPIO
from LCD_IC2_classe import LCD_I2C
from Entrada_Nombre_Classe import EntradaDatos

# Configuración de pines GPIO
PIN_BOTON1 = 18  # Botón confirmar
PIN_BOTON2 = 19  # Botón avanzar
PIN_BOTON3 = 21  # Botón retroceder

# Limpieza previa de pines GPIO
try:
    GPIO.cleanup()
except RuntimeWarning:
    pass  # Ignora el error si ya están limpios

# Inicializar botones
b_confirma = Button(PIN_BOTON1, bounce_time=0.02, pull_up=True, hold_time=3)
b_adelante = Button(PIN_BOTON2, bounce_time=0.02, pull_up=True)
b_atras = Button(PIN_BOTON3, bounce_time=0.02, pull_up=True)

# Crear LCD
lcd = LCD_I2C()

# Crear instancia única de EntradaDatos
entrada_datos = EntradaDatos(
    pin_boton_adelante=b_adelante,
    pin_boton_atras=b_atras,
    pin_boton_confirmar=b_confirma,
    lcd=lcd,
    modo="nombre"  # Modo inicial
)

# Variables globales para guardar los datos
nombre = ""
cantidad = ""
tipo = ""


def finalizar_modo():
    """
    Finaliza el modo actual y pasa al siguiente.
    """
    global nombre, cantidad, tipo

    if entrada_datos.modo == "nombre":
        # Guardar el nombre capturado y pasar al siguiente modo
        global nombre
        nombre = entrada_datos.nombre.strip()
        print(f"[INFO] Nombre capturado: {nombre}")
        cambiar_modo("cantidad")

    elif entrada_datos.modo == "cantidad":
        # Guardar la cantidad capturada y pasar al siguiente modo
        global cantidad
        cantidad = entrada_datos.cantidad.strip()
        print(f"[INFO] Cantidad capturada: {cantidad}")
        cambiar_modo("tipo")

    elif entrada_datos.modo == "tipo":
        # Guardar el tipo capturado y finalizar
        global tipo
        tipo = entrada_datos.tipos_azucar[entrada_datos.indice_tipo]
        print(f"[INFO] Tipo capturado: {tipo}")
        finalizar_flujo()


def cambiar_modo(modo):
    """
    Cambia dinámicamente el modo de la instancia EntradaDatos.
    """
    print(f"[INFO] Cambiando al modo: {modo}")
    entrada_datos.modo = modo
    entrada_datos.reiniciar_datos()  # Reinicia los datos para el nuevo modo
    entrada_datos.mostrar_estado()  # Actualiza el LCD con el nuevo modo


def finalizar_flujo():
    """
    Finaliza el flujo y muestra los resultados capturados.
    """
    lcd.clear()
    lcd.write("Datos capturados:", line=1)
    lcd.write(f"{nombre}, {cantidad}, {tipo}", line=2)
    print(f"[INFO] Datos finales: Nombre: {nombre}, Cantidad: {cantidad}, Tipo: {tipo}")

try:
    print("[INFO] Iniciando flujo de captura.")

    while True:

        if entrada_datos.finalizado:
            print(f"[DEBUG] Finalizado detectado en modo: {entrada_datos.modo}")

            if entrada_datos.modo == "nombre":
                nombre = entrada_datos.nombre.strip()
                print(f"[INFO] Nombre capturado: {nombre}")
                entrada_datos.finalizado = False
                entrada_datos.modo = "cantidad"
                entrada_datos.mostrar_estado()

            elif entrada_datos.modo == "cantidad":
                cantidad = entrada_datos.cantidad.strip()
                print(f"[INFO] Cantidad capturada: {cantidad}")
                entrada_datos.finalizado = False
                entrada_datos.modo = "tipo"
                entrada_datos.mostrar_estado()

            elif entrada_datos.modo == "tipo":
                tipo = entrada_datos.tipos_azucar[entrada_datos.indice_tipo]
                print(f"[INFO] Tipo capturado: {tipo}")
                print(f"[INFO] Flujo completado: {nombre}, {cantidad}, {tipo}")
                break
        else:
            entrada_datos.run()

except KeyboardInterrupt:
    print("[INFO] Salida del programa.")
finally:
    GPIO.cleanup()
