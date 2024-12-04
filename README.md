Aquí tienes el documento convertido a formato Markdown para que lo uses como README en GitHub:

# Proyecto: Dispensador Inteligente de Azúcar

**Curso:** Prototipos IoT  
**Alumno:** Pere Martin  
**Fecha:** 05/12/2024  

---

## Introducción

El **"Dispensador Inteligente de Azúcar"** es un sistema diseñado para dispensar azúcar de manera automatizada y personalizada, utilizando tecnologías como el reconocimiento facial, sensores, motores controlados por PWM y una base de datos para registrar y gestionar las preferencias y actividades de los usuarios. Este proyecto busca no solo automatizar una tarea rutinaria, sino también explorar cómo la personalización y la tecnología pueden mejorar la experiencia del usuario en su vida diaria.

A lo largo del desarrollo, me encontré con diversos desafíos técnicos y de diseño, que abordé con un enfoque modular tanto en el hardware como en el software. El objetivo final fue crear un sistema que pudiera reconocer a los usuarios, identificar sus preferencias almacenadas y dispensar la cantidad exacta de azúcar deseada en función de esas configuraciones.

---

## Motivación del Proyecto

La idea detrás del proyecto fue llevar la personalización a un contexto práctico mediante el uso de tecnologías de inteligencia artificial e Internet de las cosas (IoT). En un mundo donde la experiencia personalizada se está convirtiendo en un estándar, integrar sistemas de reconocimiento facial con dispositivos cotidianos abre un abanico de posibilidades. Por ejemplo:

- Personalizar la cantidad de azúcar en bebidas según las preferencias individuales.
- Ajustar automáticamente la cantidad de café en una máquina.
- Extender este modelo a otras áreas como el control de porciones de alimentos o ingredientes en cocinas automatizadas.

Este proyecto no solo tiene un enfoque funcional, sino que también sirve como una plataforma para explorar cómo las tecnologías emergentes pueden integrarse en entornos cotidianos. Además, proporciona una base sólida para futuras mejoras, como incluir nuevos ingredientes o expandir las capacidades del sistema.

---

## Estructura General del Sistema

El sistema está compuesto por varios módulos principales, cada uno con una funcionalidad específica que, al combinarse, permiten el funcionamiento integral del dispensador. A continuación, se describen los elementos clave:

### 1. Reconocimiento Facial

El reconocimiento facial es el núcleo del sistema. Utiliza una cámara conectada a una Raspberry Pi que identifica al usuario mediante librerías como `dlib` y `OpenCV`. Cada usuario tiene un perfil que incluye:

- Su encoding facial (generado por `dlib`).
- Sus preferencias de tipo de azúcar y cantidad (almacenadas en la base de datos).

**Desafíos en esta parte:**  
Implementar `dlib` en la Raspberry Pi fue complejo debido a las limitaciones de recursos del dispositivo. Esto me llevó a crear una imagen Debian optimizada para incluir las dependencias necesarias y reducir la carga de procesamiento.

### 2. Interfaz de Usuario con Pulsadores y Pantalla LCD

La interacción con el usuario se realiza mediante pulsadores y una pantalla LCD conectada mediante el protocolo I2C. Esta pantalla muestra mensajes en tiempo real, como:

- Instrucciones iniciales: “Sistema listo. Reconociendo usuario.”
- Solicitudes de entrada: “Ingrese número de cucharadas (en gramos): _”.
- Notificaciones: “Dispensando azúcar moreno…” o “Coloque una taza para continuar.”

El sistema permite que el usuario ajuste manualmente la cantidad de azúcar utilizando los pulsadores si lo desea. Sin embargo, esta funcionalidad quedó parcialmente desarrollada para registrar nuevos usuarios y configuraciones completas desde la interfaz física.

### 3. Sensores Infrarrojos

Para garantizar que el azúcar no se dispense sin un recipiente debajo, se integró un sensor infrarrojo. Este componente detecta la presencia de una taza bajo el dispensador y, si no está presente, bloquea el proceso y muestra un mensaje de error en la pantalla LCD. Esto asegura un uso eficiente del sistema y evita desperdicios.

### 4. Motores DC y Control de Dispensado

Cada tipo de azúcar está asociado a un motor DC independiente, controlado mediante señales PWM. Estos motores regulan una trampilla que dispensa el azúcar desde un embudo hacia el recipiente. La cantidad dispensada se calcula en función del tiempo de activación del motor, lo que permite una dosificación precisa.

**Problema:**  
La estructura inicial, hecha de cartón, no proporcionaba la rigidez necesaria para mantener un espacio constante de **1 mm**, lo que resultaba en pérdidas de azúcar o cantidades inexactas. Este problema subrayó la necesidad de usar materiales más robustos en futuras versiones.

---

## Base de Datos en MariaDB

La base de datos es el corazón del sistema, donde se almacena toda la información relacionada con los usuarios, los tipos de azúcar y las actividades realizadas. Utilicé MariaDB en la Raspberry Pi y la gestioné desde Python mediante `mysql-connector`.

### Estructura de la Base de Datos

1. **usuarios**:  
   Almacena los datos básicos de los usuarios, como su nombre, apellidos, fecha de registro y su tipo de azúcar predeterminado.

2. **tipo_azucar**:  
   Contiene los tipos de azúcar disponibles en el sistema (Blanco, Moreno, Edulcorante).

3. **actividad**:  
   Registra cada acción realizada en el dispensador, incluyendo el usuario que lo utilizó, el tipo de azúcar dispensado, la fecha y la cantidad servida.

---

## Clases Utilizadas en el Proyecto

El diseño del software es modular, lo que facilita el mantenimiento y las futuras expansiones. A continuación, se describen las principales clases implementadas:

1. **FaceRecognitionClass**:
   - Gestiona el reconocimiento facial utilizando `dlib` y `OpenCV`.
   - Genera y almacena encodings faciales en la base de datos.
   - Se encarga de identificar al usuario al inicio del proceso.

2. **LCD_I2C**:
   - Controla la pantalla LCD conectada mediante el protocolo I2C.
   - Muestra mensajes en tiempo real y actúa como el principal medio de comunicación con el usuario.

3. **SensorInfrarrojo**:
   - Detecta la presencia de un recipiente bajo el dispensador.
   - Envía señales al sistema para permitir o bloquear el dispensado.

4. **MotorDC**:
   - Controla los motores responsables de abrir y cerrar las trampillas de los embudos.
   - Utiliza PWM para dosificar con precisión la cantidad de azúcar.

5. **ContenedorClass**:
   - Supervisa el estado lleno/vacío de los contenedores de azúcar.
   - Registra cada dispensado en la base de datos y emite alertas cuando el nivel es bajo.

6. **EntradaDatos**:
   - Permite la interacción del usuario mediante pulsadores.
   - Facilita la introducción de datos como el tipo y cantidad de azúcar deseada.

---

## Problemas y Desafíos Durante el Desarrollo

### 1. Instalación de Dlib

Instalar `dlib` en la Raspberry Pi fue complicado debido a sus altos requisitos de memoria y procesamiento. Tras varios intentos fallidos, creé una imagen Debian personalizada para reducir la carga del sistema operativo y optimizar el rendimiento.

### 2. Entrada de Datos

La funcionalidad de entrada de datos desde pulsadores quedó incompleta debido a la falta de tiempo y a la complejidad de diseñar una interfaz fluida sin teclado físico.

### 3. Diseño Mecánico

El prototipo inicial de cartón no era suficientemente robusto, lo que generó problemas de alineación y estabilidad. En futuras versiones, sería ideal usar materiales más resistentes como madera o plástico.

---

## Reflexión General

Cada desafío del proyecto me permitió aprender y mejorar habilidades tanto técnicas como de planificación. La instalación de `dlib` me enseñó la importancia de preparar adecuadamente el entorno de desarrollo. Los problemas mecánicos subrayaron la relevancia de usar materiales adecuados desde el principio. Este proyecto establece una base sólida para continuar innovando y expandiendo sus capacidades.

Copia y pega este texto directamente en el archivo README.md de tu repositorio en GitHub. Avísame si necesitas algo más o ajustes adicionales. 😊
