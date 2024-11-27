from Sensor_infrarrojos_classe import SensorInfrarrojo

class Taza:
    def __init__(self, pin_sensor):
        """
        Inicializa la clase Taza con un sensor infrarrojo.
        
        :param pin_sensor: Pin GPIO conectado al sensor infrarrojo.
        """
        self.sensor = SensorInfrarrojo(pin_sensor)

    def taza_presente(self):
        """
        Verifica si la taza está correctamente colocada usando el sensor infrarrojo.
        
        :return: True si la taza está en posición, False en caso contrario.
        """
        return self.sensor.objeto_detectado()

    def esperar_por_taza(self):
        """
        Espera hasta que la taza esté correctamente colocada.
        """
        print("[INFO] Esperando por la taza...")
        while not self.taza_presente():
            time.sleep(0.1)  # Evitar demasiados bucles rápidos
        print("[INFO] Taza detectada.")

    def limpiar(self):
        """
        Limpia los recursos del sensor infrarrojo.
        """
        self.sensor.limpiar()

# Ejemplo de uso con la clase Taza:
if __name__ == "__main__":
    taza = Taza(pin_sensor=17)  # Cambia al pin GPIO conectado al sensor infrarrojo
    try:
        taza.esperar_por_taza()
        print("[INFO] Proceso completado.")
    except KeyboardInterrupt:
        print("[INFO] Finalizando...")
    finally:
        taza.limpiar()