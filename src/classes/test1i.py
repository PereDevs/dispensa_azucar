from gpiozero import Button

# Configura el botón en GPIO 18
button = Button(18, pull_up=True)

while True:
    if button.is_pressed:
        print("¡Botón presionado!")
    else:
        print("Botón no presionado")
