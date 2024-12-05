```markdown
# **Proyecto: Dispensador Inteligente de Azúcar**
**Curso:** Prototipos IoT con Raspberry  
**Alumno:** Pere Martin  
**Fecha:** 05/12/2024  

---

## **Introducción**

El **“Dispensador Inteligente de Azúcar”** es un sistema diseñado para dispensar azúcar de manera automatizada y personalizada, utilizando tecnologías como el **reconocimiento facial**, sensores, motores controlados por PWM y una base de datos para registrar y gestionar las preferencias y actividades de los usuarios. Este proyecto busca no solo automatizar una tarea rutinaria, sino también explorar cómo la personalización y la tecnología pueden mejorar la experiencia del usuario en su vida diaria.

A lo largo del desarrollo, me encontré con diversos desafíos técnicos y de diseño, que abordé con un enfoque modular tanto en el hardware como en el software. El objetivo final fue crear un sistema que pudiera **reconocer a los usuarios**, identificar sus preferencias almacenadas y dispensar la cantidad exacta de azúcar deseada en función de esas configuraciones.

---

## **Motivación del Proyecto**

La idea detrás del proyecto fue llevar la personalización a un contexto práctico mediante el uso de tecnologías de inteligencia artificial e **Internet de las Cosas (IoT)**. En un mundo donde la experiencia personalizada se está convirtiendo en un estándar, integrar sistemas de reconocimiento facial con dispositivos cotidianos abre un abanico de posibilidades. Por ejemplo:
- **Personalizar la cantidad de azúcar** en bebidas según las preferencias individuales.
- Ajustar automáticamente la cantidad de café en una máquina.
- Extender este modelo a otras áreas como el control de porciones de alimentos o ingredientes en cocinas automatizadas.

Este proyecto no solo tiene un enfoque funcional, sino que también sirve como una plataforma para explorar cómo las tecnologías emergentes pueden integrarse en entornos cotidianos. Además, proporciona una base sólida para futuras mejoras, como incluir nuevos ingredientes o expandir las capacidades del sistema.

---

## **Estructura General del Sistema**

El sistema está compuesto por varios módulos principales, cada uno con una funcionalidad específica que, al combinarse, permiten el funcionamiento integral del dispensador. A continuación, se describen los elementos clave:

### **1. Reconocimiento Facial**

El **reconocimiento facial** es el núcleo del sistema. Utiliza una cámara conectada a una Raspberry Pi que identifica al usuario mediante librerías como **dlib** y **OpenCV**. Cada usuario tiene un perfil que incluye:
- Su **encoding facial** (generado por dlib).
- Sus preferencias de tipo de azúcar y cantidad (almacenadas en la base de datos).

**Desafíos:**
- **Instalación de dlib** en la Raspberry Pi, que fue compleja debido a las limitaciones de recursos. Esto implicó crear una imagen Debian optimizada para reducir la carga de procesamiento.

---

### **2. Interfaz de Usuario con Pulsadores y Pantalla LCD**

La interacción con el usuario se realiza mediante **pulsadores** y una **pantalla LCD conectada mediante el protocolo I2C**. Esta pantalla muestra mensajes como:
- **Instrucciones iniciales:** “Sistema listo. Reconociendo usuario.”
- **Solicitudes de entrada:** “Ingrese número de cucharadas (en gramos): _”.
- **Notificaciones:** “Dispensando azúcar moreno…” o “Coloque una taza para continuar.”

**Limitaciones:** La funcionalidad de registrar nuevos usuarios y configuraciones quedó parcialmente desarrollada.

---

### **3. Sensores Infrarrojos**

Para garantizar que el azúcar no se dispense sin un recipiente debajo, se integró un **sensor infrarrojo**. Este componente asegura:
- Detectar la presencia de una taza bajo el dispensador.
- Bloquear el proceso si no hay recipiente y mostrar un mensaje de error.

---

### **4. Motores DC y Control de Dispensado**

Cada tipo de azúcar está asociado a un **motor DC independiente**, controlado mediante señales **PWM**. Estos motores regulan una trampilla que dispensa el azúcar desde un embudo hacia el recipiente.

**Problemas:**
- La estructura inicial de cartón no proporcionaba la rigidez necesaria, lo que afectó la precisión del dispensado.

---

### **Base de Datos en MariaDB**

La base de datos, implementada en **MariaDB**, almacena toda la información sobre:
1. **Usuarios:** Datos básicos como nombre, tipo de azúcar predeterminado.
2. **Tipos de azúcar:** Blanco, Moreno, Edulcorante.
3. **Actividad:** Registros de acciones realizadas por el dispensador.

---

## **Clases Utilizadas en el Proyecto**

1. **FaceRecognitionClass:**  
   Gestiona el reconocimiento facial utilizando dlib y OpenCV.
2. **LCD_I2C:**  
   Controla la pantalla LCD y muestra mensajes en tiempo real.
3. **SensorInfrarrojo:**  
   Detecta la presencia de recipientes.
4. **MotorDC:**  
   Controla los motores responsables de dosificar el azúcar.
5. **ContenedorClass:**  
   Supervisa el estado de los contenedores y emite alertas.
6. **EntradaDatos:**  
   Permite la interacción del usuario mediante pulsadores.

---

## **Problemas y Desafíos Durante el Desarrollo**

### **1. Instalación de Dlib**
- **Problemas:** Falta de memoria RAM, dependencias rotas y errores de configuración.
- **Solución:** Crear una imagen Debian personalizada con librerías esenciales.

### **2. Entrada de Datos**
- **Problemas:** Complejidad de la interfaz con pulsadores y falta de tiempo para completar la lógica necesaria.
- **Reflexión:** Priorizar funcionalidades clave sobre características secundarias.

### **3. Diseño Mecánico**
- **Problemas:** Uso de cartón, que resultó inadecuado por su falta de rigidez.
- **Solución:** Considerar materiales más robustos como madera o plástico en futuras iteraciones.

---

## **Reflexión General**

Este proyecto fue una oportunidad para aprender y mejorar habilidades técnicas y de planificación. Aunque enfrenté múltiples desafíos, cada uno aportó lecciones valiosas sobre la importancia de:
- Preparar adecuadamente el entorno de desarrollo.
- Priorizar funcionalidades clave en proyectos limitados por tiempo.
- Elegir materiales adecuados desde el inicio para evitar problemas mecánicos.

El **“Dispensador Inteligente de Azúcar”** representa una base sólida para futuras mejoras y demuestra el potencial de integrar tecnologías emergentes en la vida cotidiana.
```
