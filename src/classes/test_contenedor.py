from gpiozero import Button

# Configura el botón en GPIO 18 con pull-down
button = Button(18, pull_up=True)

print("Estado inicial:", "Presionado" if button.is_pressed else "No presionado")

while True:
    if button.is_pressed:
        print("¡Botón presionado!")
    else:
        print("Botón no presionado")
