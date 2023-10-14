import RPi.GPIO as GPIO
from time import sleep

class semaforo:
    def __init__(self, n_semaforo, pino1, pino2):
        self.n_semaforo = n_semaforo
        self.pino1 = pino1
        self.pino2 = pino2
        GPIO.setup(self.pino1, GPIO.OUT)
        GPIO.setup(self.pino2, GPIO.OUT)

    def verde(self):
        GPIO.output(self.pino1, GPIO.LOW)
        GPIO.output(self.pino2, GPIO.HIGH)

    def amarelo(self):
        GPIO.output(self.pino1, GPIO.HIGH)
        GPIO.output(self.pino2, GPIO.LOW)

    def vermelho(self):
        GPIO.output(self.pino1, GPIO.HIGH)
        GPIO.output(self.pino2, GPIO.HIGH)

    def desligado(self):
        GPIO.output(self.pino1, GPIO.LOW)
        GPIO.output(self.pino2, GPIO.LOW)

    def pare(self):
        self.vermelho()

    def atencao(self):
        self.amarelo()
    
    def passe(self):
        self.verde()
    
    def desliga_semaforo(self):
        self.desligado()

""" #Testar Semaforos funcionando   
def main():
    GPIO.setmode(GPIO.BCM)
    semaforo1 = semaforo("Semaforo 1", 10, 8)  # Substitua os pinos 17 e 18 pelos pinos que você está usando
    semaforo2 = semaforo("Semaforo 2", 1, 18)  # Substitua os pinos 22 e 23 pelos pinos que você está usando

    try:
        while True:
            semaforo1.passe()
            time.sleep(5)
            semaforo1.atencao()
            time.sleep(2)
            semaforo1.pare()
            time.sleep(2)

            semaforo2.pare()
            time.sleep(2)
            semaforo2.atencao()
            time.sleep(2)
            semaforo2.passe()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
        
""" 