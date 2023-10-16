import RPi.GPIO as GPIO
#import time

class botao_pedestre:
    def __init__(self, botao_pedestre):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(botao_pedestre, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.botao_pedestre = botao_pedestre
        self.pedestre_esperando = False
        GPIO.add_event_detect(botao_pedestre, GPIO.RISING, callback=self.set_pedestre_esperando, bouncetime=300)

    def set_pedestre_esperando(self, channel):
        self.pedestre_esperando = True

    def set_pedestre_passando(self):
        self.pedestre_esperando = False

    def get_pedestre_esperando(self):
        return self.pedestre_esperando
"""
#Testar Botao funcionando 
    def main():
        botao_pedestre = botao_pedestre(13)  #13, 19, 23, 24
        try:
            while True:
                if botao_pedestre.get_pedestre_esperando():
                    print("Pedestre esperando")
                else:
                    print("Pedestre não está esperando")
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    main()
    
"""