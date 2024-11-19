# Dispensador Inteligente de Azúcar

## Descripción

Este proyecto consiste en un dispensador de azúcar inteligente que utiliza una Raspberry Pi y una cámara para reconocer la cara del usuario y dispensar de forma precisa el tipo y la cantidad de azúcar deseado directamente en la taza. El dispositivo está diseñado para ofrecer una experiencia personalizada, rápida y eficiente.

## Características

- **Reconocimiento Facial**: La cámara integrada identifica al usuario y selecciona automáticamente el tipo y la cantidad de azúcar basada en sus preferencias.
- **Variedades de Azúcar**:
  - Azúcar blanco
  - Azúcar moreno
  - Edulcorante
- **Interfaz Amigable**: El dispositivo está diseñado para ser fácil de usar, con un proceso completamente automatizado.
- **Dispensación Precisa**: Detecta la posición de la taza y dispensa la cantidad exacta en el lugar correcto.

## Componentes Principales

- **Hardware**:
  - Raspberry Pi (modelo recomendado: Raspberry Pi 4)
  - Cámara compatible con Raspberry Pi
  - Motores para controlar los dispensadores
  - Sensores de proximidad para detectar la taza
  - Contenedores para las tres variedades de azúcar

- **Software**:
  - Reconocimiento facial utilizando OpenCV y `face-recognition`
  - Control de motores mediante GPIO
  - Script Python para la lógica de dispensación

## Funcionamiento

1. **Reconocimiento Facial**:
   - Al colocarse frente al dispositivo, la cámara identifica al usuario.
   - Si el usuario ya está registrado, se cargan sus preferencias.
