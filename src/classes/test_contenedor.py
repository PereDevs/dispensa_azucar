from gpiozero import Button
from signal import pause


# Configura el botón en GPIO 18 con pull-down
boton1 = Button(18, pull_up=True)
boton2 = Button(19, pull_up=True)
boton3 = Button(13, pull_up=True)


def verificar_botones():
    if boton1.is_pressed and boton2.is_pressed:
        print("Boton 1 y 2 están pulsados")
    elif boton1.is_pressed and boton2.is_pressed:
        print("Todos están pulsados")
    elif boton1.is_pressed:
        print("Botón 1 está pulsado")
    elif boton2.is_pressed:
        print("Botón 2 está pulsado")
    elif boton3.is_pressed:
        print("Botón 3 está pulsado")
    else:
        print("Ningún botón está pulsado")

# Detectar cuando cualquier botón cambia de estado
boton1.when_pressed = verificar_botones
boton2.when_pressed = verificar_botones
boton3.when_pressed = verificar_botones


# Mantener el script ejecutándose
pause()
