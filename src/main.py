from graphviz import Digraph

# Crear el objeto del diagrama de flujo
flowchart = Digraph(format='png', name='Dispensador_Inteligente_Azucar')
flowchart.attr(rankdir='TB', size='8,10')

# Definir nodos principales
flowchart.node('start', 'Inicio del sistema\n- Inicializar componentes\n- Cargar base de datos', shape='ellipse')
flowchart.node('taza', '¿Taza en su lugar?', shape='diamond')
flowchart.node('taza_no', 'Notificar: "Coloque la taza"', shape='box')
flowchart.node('camara', 'Capturar imagen\n(Reconocimiento facial)', shape='box')
flowchart.node('rostro', '¿Se detecta un rostro?', shape='diamond')
flowchart.node('reintentar', 'Reintentar captura\n(Max 3 intentos)', shape='box')
flowchart.node('rostro_no', 'Notificar: "No se detecta rostro"', shape='box')
flowchart.node('registro', '¿Usuario registrado?', shape='diamond')
flowchart.node('manual', 'Solicitar selección manual\n(Tipo y cantidad de azúcar)', shape='box')
flowchart.node('preferencias', 'Cargar preferencias\n(Tipo y cantidad)', shape='box')
flowchart.node('azucar', '¿Azúcar suficiente?', shape='diamond')
flowchart.node('sin_azucar', 'Notificar: "Falta azúcar"\nEsperar recarga', shape='box')
flowchart.node('dispensar', 'Activar dispensador\n(Dispensar cantidad exacta)', shape='box')
flowchart.node('motor', '¿Motor funcionando correctamente?', shape='diamond')
flowchart.node('error_motor', 'Detener proceso\nNotificar error', shape='box')
flowchart.node('notificar', 'Notificar al usuario:\n"Tu azúcar está listo"', shape='box')
flowchart.node('fin', 'Fin del proceso\nReiniciar sistema', shape='ellipse')

# Definir las conexiones
flowchart.edges([
    ('start', 'taza'),
    ('taza', 'taza_no', {'label': 'No'}),
    ('taza', 'camara', {'label': 'Sí'}),
    ('taza_no', 'taza'),
    ('camara', 'rostro'),
    ('rostro', 'reintentar', {'label': 'No'}),
    ('reintentar', 'camara'),
    ('rostro', 'registro', {'label': 'Sí'}),
    ('registro', 'manual', {'label': 'No'}),
    ('registro', 'preferencias', {'label': 'Sí'}),
    ('manual', 'azucar'),
    ('preferencias', 'azucar'),
    ('azucar', 'sin_azucar', {'label': 'No'}),
    ('azucar', 'dispensar', {'label': 'Sí'}),
    ('sin_azucar', 'azucar'),
    ('dispensar', 'motor'),
    ('motor', 'error_motor', {'label': 'No'}),
    ('motor', 'notificar', {'label': 'Sí'}),
    ('notificar', 'fin')
])

# Renderizar el diagrama
output_path = '/mnt/data/Dispensador_Inteligente_Azucar'
flowchart.render(output_path, format='png', cleanup=True)

output_path + '.png'



