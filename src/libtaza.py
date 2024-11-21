import distancia_classe 
import RPi.GPIO as GPIO
import time


# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)



class DetectaTaza():

    def __init__(self):
        pass
    
    def taza_posicion():
        
        # Define GPIO pins for the sensor
        
        try:
            TRIG_PIN = 23  # GPIO23 (change as needed)
            ECHO_PIN = 24  # GPIO24 
            # Set up the GPIO pins
            GPIO.setup(TRIG_PIN, GPIO.OUT)
            GPIO.setup(ECHO_PIN, GPIO.IN)
            
            sensor = distancia_classe.SensorDistancia
            distancia = sensor.mesura_distancia()
            if distancia > 3:
                print("Coloca la taza más cerca del sensor")
                return False
            else:
                return True
            
        except:
            print("Se podujo un error")
            
            
        
    
