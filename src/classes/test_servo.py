from servo_class import ServoMotor
import time

if __name__ == "__main__":
    servo = ServoMotor(pin=23)  # Define el GPIO conectado al servo
    try:
        servo.open_trapdoor()
#        time.sleep(1)  # Tiempo que permanece abierto
        servo.close_trapdoor()
    finally:
        servo.cleanup()