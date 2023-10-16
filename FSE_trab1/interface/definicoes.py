import RPi.GPIO as GPIO
from time import sleep
import threading

# Configurar a biblioteca RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dicionário para mapear os pinos de acordo com a descrição
gpio_pins = {
    # GPIO Cruzamento 1
    "semaforo1_pino1_c1": 9,
    "semaforo1_pino2_c1": 11,
    "semaforo2_pino1_c1": 5,
    "semaforo2_pino2_c1": 6,
    "botao_pedestre1_c1": 13,
    "botao_pedestre2_c1": 19,
    "sensor_auxiliar1_c1": 26,
    "sensor_auxiliar2_c1": 22,
    "sensor_principal1_c1": 0,
    "sensor_principal2_c1": 27,
    "buzzer_c1": 17,

    # GPIO Cruzamento 2
    "semaforo1_pino1_c2": 10,
    "semaforo1_pino2_c2": 8,
    "semaforo2_pino1_c2": 1,
    "semaforo2_pino2_c2": 18,
    "botao_pedestre1_c2": 23,
    "botao_pedestre2_c2": 24,
    "sensor_auxiliar1_c2": 25,
    "sensor_auxiliar2_c2": 12,
    "sensor_principal1_c2": 16,
    "sensor_principal2_c2": 20,
    "buzzer_c2": 21
}

# Inicializar pinos GPIO
for pin in gpio_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Definição dos botões de pedestres
botao_pedestre1_c1 = gpio_pins["botao_pedestre1_c1"]
botao_pedestre2_c1 = gpio_pins["botao_pedestre2_c1"]
botao_pedestre1_c2 = gpio_pins["botao_pedestre1_c2"]
botao_pedestre2_c2 = gpio_pins["botao_pedestre2_c2"]

# Definição dos buzzers
buzzer_c1 = gpio_pins["buzzer_c1"]
buzzer_c2 = gpio_pins["buzzer_c2"]

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

def semaforo1_c1_desligado():
    GPIO.output(gpio_pins["semaforo1_pino1_c1"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo1_pino2_c1"], GPIO.LOW)

def semaforo2_c1_verde():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.HIGH)

def semaforo2_c1_amarelo():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.LOW)

def semaforo2_c1_vermelho():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.HIGH)

def semaforo2_c1_desligado():
    GPIO.output(gpio_pins["semaforo2_pino1_c1"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c1"], GPIO.LOW)

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

def semaforo1_c2_desligado():
    GPIO.output(gpio_pins["semaforo1_pino1_c2"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo1_pino2_c2"], GPIO.LOW)

def semaforo2_c2_verde():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.HIGH)

def semaforo2_c2_amarelo():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.LOW)

def semaforo2_c2_vermelho():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.HIGH)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.HIGH)

def semaforo2_c2_desligado():
    GPIO.output(gpio_pins["semaforo2_pino1_c2"], GPIO.LOW)
    GPIO.output(gpio_pins["semaforo2_pino2_c2"], GPIO.LOW)


# Função para ligar o Buzzer do cruzamento 1
def buzzer_c1_on():
    GPIO.output(gpio_pins["buzzer_c1"], GPIO.HIGH)

# Função para desligar o Buzzer do cruzamento 1
def buzzer_c1_off():
    GPIO.output(gpio_pins["buzzer_c1"], GPIO.LOW)

# Função para ligar o Buzzer do cruzamento 2
def buzzer_c2_on():
    GPIO.output(gpio_pins["buzzer_c2"], GPIO.HIGH)

# Função para desligar o Buzzer do cruzamento 2
def buzzer_c2_off():
    GPIO.output(gpio_pins["buzzer_c2"], GPIO.LOW)


def cruzamento1_modo_diurno():
    estado_botao_pedestre1_c1 = False
    estado_botao_pedestre2_c1 = False

    if GPIO.input(botao_pedestre1_c1) == GPIO.HIGH:
            estado_botao_pedestre1_c1 = True

    if GPIO.input(botao_pedestre2_c1) == GPIO.HIGH:
            estado_botao_pedestre2_c1 = True

    # Cruzamento 1
    while True:
        #Principal verde/Auxiliar vermelho....................................
        semaforo1_c1_verde()
        semaforo2_c1_vermelho()
        sleep(10)
        if estado_botao_pedestre1_c1 == True:
            #mudando (aparecendo o amarelo)
            semaforo1_c1_amarelo()
            semaforo2_c1_vermelho()
            buzzer_c1_on()
            sleep(2)
            buzzer_c1_off()
            estado_botao_pedestre1_c1 = False
            #Botao volta a nao estar acionado para o proximo ciclo
        else:
            sleep(10)
            #mudando (aparecendo o amarelo)
            semaforo1_c1_amarelo()
            semaforo2_c1_vermelho()
            buzzer_c1_on()
            sleep(2)
            buzzer_c1_off()
        
        #Auxiliar verde/Principal vermelho....................................
        semaforo1_c1_vermelho()
        semaforo2_c1_verde()
        sleep(5)  
        if estado_botao_pedestre2_c1 == True:
            #mudando (aparecendo o amarelo)
            semaforo1_c1_vermelho()
            semaforo2_c1_amarelo()
            buzzer_c1_on()
            sleep(2)
            buzzer_c1_off()
            estado_botao_pedestre2_c1 = False
            #Botao volta a nao estar acionado para o proximo ciclo
             
        else:
            sleep(5)
            #mudando (aparecendo o amarelo)
            semaforo1_c1_vermelho()
            semaforo2_c1_amarelo()
            buzzer_c1_on()
            sleep(2)
            buzzer_c1_off()

def cruzamento1_modo_emergencia():
    # Cruzamento 1
    while True:
        semaforo1_c1_verde()
        semaforo2_c1_vermelho()

def cruzamento1_modo_noturno():
    # Cruzamento 1
    while True:
        semaforo1_c1_amarelo()
        semaforo2_c1_amarelo()
        sleep(1)

        semaforo1_c1_desligado()
        semaforo2_c1_desligado()
        sleep(1)




def cruzamento2_modo_diurno():
    estado_botao_pedestre1_c2 = False
    estado_botao_pedestre2_c2 = False

    if GPIO.input(botao_pedestre1_c2) == GPIO.HIGH:
                estado_botao_pedestre1_c2 = True

    if GPIO.input(botao_pedestre2_c2) == GPIO.HIGH:
                estado_botao_pedestre2_c2 = True
    # Cruzamento 2
    while True:
        semaforo1_c2_verde()
        semaforo2_c2_vermelho()
        sleep(10)
        if estado_botao_pedestre1_c2 == True:
            #mudando (aparecendo o amarelo)
            semaforo1_c2_amarelo()
            semaforo2_c2_vermelho()
            buzzer_c2_on()
            sleep(2)
            buzzer_c2_off()
            estado_botao_pedestre1_c2 = False
            #Botao volta a nao estar acionado para o proximo ciclo
        else:
            sleep(10)
            #mudando (aparecendo o amarelo)
            semaforo1_c2_amarelo()
            semaforo2_c2_vermelho()
            buzzer_c2_on()
            sleep(2)
            buzzer_c2_off()
            estado_botao_pedestre1_c2 = False
            #Botao volta a nao estar acionado para o proximo ciclo

        semaforo1_c2_vermelho()
        semaforo2_c2_verde()
        sleep(5)
        if estado_botao_pedestre2_c2 == True:
            #mudando (aparecendo o amarelo)
            semaforo1_c2_vermelho()
            semaforo2_c2_amarelo()
            buzzer_c2_on()
            sleep(2)
            buzzer_c2_off()
            estado_botao_pedestre2_c2 = False
            #Botao volta a nao estar acionado para o proximo ciclo
             
        else:
            sleep(5)
            #mudando (aparecendo o amarelo)
            semaforo1_c2_vermelho()
            semaforo2_c2_amarelo()
            buzzer_c2_on()
            sleep(2)
            buzzer_c2_off()
            estado_botao_pedestre2_c2 = False
            #Botao volta a nao estar acionado para o proximo ciclo
    
def cruzamento2_modo_emergencia():
    # Cruzamento 1
    while True:
        semaforo1_c2_verde()
        semaforo2_c2_vermelho()

def cruzamento2_modo_noturno():
    # Cruzamento 1
    while True:
        semaforo1_c2_amarelo()
        semaforo2_c2_amarelo()
        sleep(1)

        semaforo1_c2_desligado()
        semaforo2_c2_desligado()
        sleep(1)


# Crie threads para executar as funções dos cruzamentos em paralelo
thread_cruzamento1 = threading.Thread(target=cruzamento1_modo_diurno)
thread_cruzamento2 = threading.Thread(target=cruzamento2_modo_diurno)

# Inicie as threads
thread_cruzamento1.start()
thread_cruzamento2.start()

# Aguarde as threads terminarem (você pode ajustar isso conforme necessário)
thread_cruzamento1.join()
thread_cruzamento2.join()

# Cleanup GPIO ao final do programa
GPIO.cleanup()