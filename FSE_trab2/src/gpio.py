import logging

import RPi.GPIO as GPIO
from time import sleep
from pid import PID
import cmds

class GPIOController:
    def __init__(self):
        # Configuração para ignorar mensagens de aviso do RPi.GPIO
        GPIO.setwarnings(False)
        logging.getLogger("RPi.GPIO").setLevel(logging.ERROR)

        # Configuração dos pinos GPIO
        self.DIR1_PIN = 20  # GPIO 20 (BCM) ou Pino 38 (Board)
        self.DIR2_PIN = 21  # GPIO 21 (BCM) ou Pino 40 (Board)
        self.PWM_PIN = 12   # GPIO 12 (BCM) ou Pino 32 (Board)
        self.SENSOR_TERREO_PIN = 18  # GPIO 18 (BCM) ou Pino 12 (Board)
        self.SENSOR_1_ANDAR_PIN = 23 # GPIO 23 (BCM) ou Pino 16 (Board)
        self.SENSOR_2_ANDAR_PIN = 24 # GPIO 24 (BCM) ou Pino 18 (Board)
        self.SENSOR_3_ANDAR_PIN = 25 # GPIO 25 (BCM) ou Pino 22 (Board)

        # Configuração da biblioteca RPi.GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR1_PIN, GPIO.OUT)
        GPIO.setup(self.DIR2_PIN, GPIO.OUT)
        GPIO.setup(self.PWM_PIN, GPIO.OUT)
        GPIO.setup(self.SENSOR_TERREO_PIN, GPIO.IN)
        GPIO.setup(self.SENSOR_1_ANDAR_PIN, GPIO.IN)
        GPIO.setup(self.SENSOR_2_ANDAR_PIN, GPIO.IN)
        GPIO.setup(self.SENSOR_3_ANDAR_PIN, GPIO.IN)

        self.motor_pwm = GPIO.PWM(self.PWM_PIN, 1000)
        self.status = None

        self.terreo = None
        self.andar1 = None
        self.andar2 = None
        self.andar3 = None

        self.andar_atual = None
        self.nome_andar = None
        self.vel = None


    # Funções
    def start_pwm(self):
        self.motor_pwm.start(100)

    def stop_pwm(self):
        self.motor_pwm.stop()

    def definir_potencia_motor(self, potencia_percentual):
        self.motor_pwm.ChangeDutyCycle(potencia_percentual)

    def aciona_motor(self, sentido, potencia_percentual = 100):
        if sentido == 'sobe': 
            GPIO.output(self.DIR1_PIN, 1)
            GPIO.output(self.DIR2_PIN, 0)
            self.definir_potencia_motor(potencia_percentual)
            self.status = 'Subindo'
        elif sentido == 'desce': 
            GPIO.output(self.DIR1_PIN, 0)
            GPIO.output(self.DIR2_PIN, 1)
            self.definir_potencia_motor(potencia_percentual)
            self.status = 'Descendo'
        elif sentido == 'freio': 
            GPIO.output(self.DIR1_PIN, 1)
            GPIO.output(self.DIR2_PIN, 1)
            self.definir_potencia_motor(potencia_percentual)
            self.status = 'Parado'
        elif sentido == 'livre': 
            GPIO.output(self.DIR1_PIN, 0)
            GPIO.output(self.DIR2_PIN, 0)
            self.definir_potencia_motor(0)
            self.status = 'Parado'
    
    def ir_para_andar(self, andar):
        global pwm_global

        self.pid = PID()
        self.start_pwm()
        self.andar_atual = cmds.apurar_encoder()

        if andar == 0:
            logging.info("Indo para Terreo")
            self.pid.atualiza_referencia(self.terreo)

            if self.andar_atual - self.terreo > 40:
                while self.andar_atual > self.terreo + 40:
                    print(self.pid.controle(cmds.apurar_encoder()))
                    self.aciona_motor('Sobe', self.pid.controle(cmds.apurar_encoder()))
                    logging.debug(f"Andar atual: {self.andar_atual}")
                    sleep(0.1)
                    pwm_global = self.pid.controle(self.andar_atual)
                    cmds.apurar_pwm()
                self.stop_pwm()

        elif andar == 1:

            logging.info("Indo para 1o Andar")
            self.pid.atualiza_referencia(self.andar1)

            if self.andar_atual - self.andar1 > 40:
                while self.andar_atual > self.andar1 + 40:
                    self.andar_atual = cmds.apurar_encoder()
                    print('Andar ->', self.andar_atual)
                    print('Indo  ->',self.andar1)
                    print(self.pid.controle(cmds.apurar_encoder()))
                    self.aciona_motor('desce', abs(self.pid.controle(cmds.apurar_encoder())))
                    sleep(0.1)
                    pwm_global = self.pid.controle(self.andar_atual)
                    cmds.apurar_pwm()
                self.stop_pwm()
            elif self.andar_atual - self.andar1 < -40:
                while self.andar_atual < self.andar1 - 40:
                    self.aciona_motor('sobe', abs(self.pid.controle(cmds.apurar_encoder())))
                    logging.debug(f"Andar atual: {self.andar_atual}")
                    sleep(0.1)
                    pwm_global = self.pid.controle(self.andar_atual)
                    cmds.apurar_pwm()
                self.stop_pwm()

            self.pid.controle(self.andar_atual)

        elif andar == 2:
            logging.info("Indo para 2o Andar")
            self.pid.atualiza_referencia(self.andar2)
            self.pid.controle(self.andar_atual)

        elif andar == 3:
            logging.info("Indo para 3o Andar")
            self.pid.atualiza_referencia(self.andar3)
            self.pid.controle(self.andar_atual)

        else:
            logging.error("Andar Inexistente")
            return None
        logging.debug(f"Andar atual: {self.andar_atual}")
        self.pid.atualiza_referencia(andar)

        while True:
            self.aciona_motor('sobe', self.pid.controle(self.andar_atual))
            self.andar_atual = cmds.apurar_encoder()
            logging.debug(f"Andar atual: {self.andar_atual}")
            if self.andar_atual >= andar:
                self.stop_pwm()
                break
            sleep(0.04)

    def desce_tudo(self):
        global pwm_global

        self.start_pwm()

        while True:
            self.aciona_motor('desce')
            self.andar_atual = cmds.apurar_encoder()

            if self.andar_atual is None:
                logging.error("Falha ao obter o valor do Encoder.")
                return

            pwm_global = 100
            cmds.apurar_pwm()

            if self.andar_atual < 50:
                logging.debug(f"Andar atual: {self.andar_atual}")
                self.aciona_motor('freio')
                return

            sleep(0.04)


    def verificar_sensores(self):
        return {
            "Terreo": GPIO.input(self.SENSOR_TERREO_PIN),
            "1o Andar": GPIO.input(self.SENSOR_1_ANDAR_PIN),
            "2o Andar": GPIO.input(self.SENSOR_2_ANDAR_PIN),
            "3o Andar": GPIO.input(self.SENSOR_3_ANDAR_PIN),
        }

    def reconhece_andares(self) -> None:
        global pwm_global
        self.start_pwm()
        self.aciona_motor('sobe', 6)
        pwm_global = self.vel = 6
        sleep(0.01)

        while True:
            sensores = self.verificar_sensores()

            if sensores["Terreo"] == 1:
                logging.info("Terreo reconhecido")
                self.terreo = cmds.apurar_encoder()
                self.nome_andar = 'Terreo'

            elif sensores["1o Andar"] == 1:
                logging.info("Andar 1 reconhecido")
                self.andar1 = cmds.apurar_encoder()
                self.nome_andar = '1o Andar'

            elif sensores["2o Andar"] == 1:
                logging.info("Andar 2 reconhecido")
                self.andar2 = cmds.apurar_encoder()
                self.nome_andar = '2o Andar'

            elif sensores["3o Andar"] == 1:
                logging.info("Andar 3 reconhecido")
                self.andar3 = cmds.apurar_encoder()
                self.nome_andar = '3o Andar'

            if self.terreo and self.andar1 and self.andar2 and self.andar3:
                self.stop_pwm()
                logging.info("Andares reconhecidos")
                break

            elif self.andar3 and (
                    not self.andar3 or
                    not self.andar2 or
                    not self.andar1 or
                    not self.terreo):
                logging.debug("Tentando de novo...")
                self.aciona_motor('desce', 22)

            pwm_global = self.vel
            cmds.apurar_pwm()