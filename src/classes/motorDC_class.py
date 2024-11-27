import RPi.GPIO as GPIO
import time

class MotorDC:
    def __init__(self, in1, in2, en):
        #, en, in3=None, in4=None, en2=None):
        # Configuración de pines para el motor 1
        self.IN1 = in1
        self.IN2 = in2
        self.EN = en
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.IN1, self.IN2, self.EN], GPIO.OUT)
        '''
        # PWM para el motor 1
        self.pwm1 = GPIO.PWM(self.EN, 100)  # Configura PWM a 100 Hz
        self.pwm1.start(0)  # Inicia PWM con 0% de ciclo de trabajo

        # Si hay un segundo motor, configuramos los pines
        self.dual_motor = False
        if in3 is not None and in4 is not None and en2 is not None:
            self.IN3 = in3
            self.IN4 = in4
            self.EN2 = en2
            GPIO.setup([self.IN3, self.IN4, self.EN2], GPIO.OUT)

            # PWM para el motor 2
            self.pwm2 = GPIO.PWM(self.EN2, 100)  # Configura PWM a 100 Hz
            self.pwm2.start(0)  # Inicia PWM con 0% de ciclo de trabajo
            self.dual_motor = True
         '''
    def motor_adelante(self):
        # Motor 1 adelante
        GPIO.output(self.EN, GPIO.HIGH) # afegit meu sense pwm
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        #self.pwm1.ChangeDutyCycle(velocidad)
        '''
        # Motor 2 adelante (si está configurado)
        if self.dual_motor:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.pwm2.ChangeDutyCycle(velocidad)
        '''
    def motor_atras(self):
        # Motor 1 atrás
        GPIO.output(self.EN, GPIO.HIGH) # afegit meu sense PWM
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        # self.pwm1.ChangeDutyCycle(velocidad)
        '''
        # Motor 2 atrás (si está configurado)
        if self.dual_motor:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.pwm2.ChangeDutyCycle(velocidad)
        '''
    def motor_parar(self):
        # Detener motor 1
        GPIO.output(self.EN, GPIO.LOW) # afegit meu sense pwm
        #GPIO.output(self.IN1, GPIO.LOW)
        #GPIO.output(self.IN2, GPIO.LOW)
        #self.pwm1.ChangeDutyCycle(0)
        '''
        # Detener motor 2 (si está configurado)
        if self.dual_motor:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)
            self.pwm2.ChangeDutyCycle(0)
        ''' 
    def cleanup(self):
        '''
        # Limpieza de recursos GPIO
        self.pwm1.stop()
        if self.dual_motor:
            self.pwm2.stop()
        '''
        GPIO.cleanup()
