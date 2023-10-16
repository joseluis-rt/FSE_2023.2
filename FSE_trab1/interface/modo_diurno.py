import RPi.GPIO as GPIO
from time import sleep

# Configurar a biblioteca RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dicionário para mapear os pinos de acordo com a descrição (mantendo apenas os semáforos)
gpio_pins = {
    # GPIO Cruzamento 1
    "semaforo1_pino1_c1": 9,
    "semaforo1_pino2_c1": 11,
    "semaforo2_pino1_c1": 5,
    "semaforo2_pino2_c1": 6,

    # GPIO Cruzamento 2
    "semaforo1_pino1_c2": 10,
    "semaforo1_pino2_c2": 8,
    "semaforo2_pino1_c2": 1,
    "semaforo2_pino2_c2": 18,
}

# Inicializar pinos GPIO dos semáforos
for pin in gpio_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Cruzamento 1.................................................
def semaforo1_c1_verde():
    GPIO.output(gpio_pins["semaforo1_pino1_c1"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo1_pino2_c1"], GPIO.HIGH)

def semaforo1_c1_amarelo():
    GPIO.output(gpio_pins["semaforo1_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo1_pino2_c1"], GPIO.LOW)

def semaforo1_c1_vermelho():
    GPIO.output(gpio_pins["semaforo1_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo1_pino2_c1"], GPIO.HIGH)

def semaforo2_c1_verde():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.HIGH)

def semaforo2_c1_amarelo():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.LOW)

def semaforo2_c1_vermelho():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.HIGH)

# Cruzamento 2.................................................
def semaforo1_c2_verde():
    GPIO.output(gpio_pins["semaforo1_pino1_c2"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo1_pino2_c2"], GPIO.HIGH)

def semaforo1_c2_amarelo():
    GPIO.output(gpio_pins["semaforo1_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo1_pino2_c2"], GPIO.LOW)

def semaforo1_c2_vermelho():
    GPIO.output(gpio_pins["semaforo1_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo1_pino2_c2"], GPIO.HIGH)

def semaforo2_c2_verde():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.HIGH)

def semaforo2_c2_amarelo():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.LOW)

def semaforo2_c2_vermelho():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.HIGH)

# Função para definir o estado dos semáforos com base na temporização
def definir_temporizacao(tempo_verde_principal, tempo_verde_auxiliar, tempo_amarelo):
    while True:
        semaforo1_c1_verde()
        semaforo2_c2_vermelho()
        sleep(tempo_verde_principal)
        
        semaforo1_c1_amarelo()
        semaforo2_c2_vermelho()
        sleep(tempo_amarelo)
        
        semaforo1_c1_vermelho()
        semaforo2_c2_vermelho()
        sleep(tempo_verde_auxiliar)
        
        semaforo1_c2_verde()
        semaforo2_c1_vermelho()
        sleep(tempo_verde_principal)
        
        semaforo1_c2_amarelo()
        semaforo2_c1_vermelho()
        sleep(tempo_amarelo)
        
        semaforo1_c2_vermelho()
        semaforo2_c1_vermelho()
        sleep(tempo_verde_auxiliar)

if __name__ == "__main__":
    try:
        definir_temporizacao(10, 5, 2)  # Tempo verde principal, tempo verde auxiliar, tempo amarelo
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
