import RPi.GPIO as GPIO
import time

total_carros_passados = 0  # Variável global para rastrear o total de carros passados

class sensor:
    def __init__(self, pino_sensor, limite_velocidade, is_via_auxiliar=False):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pino_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pino_sensor = pino_sensor
        self.velocidade = 0
        self.carros_passados = 0  # Inicializa o contador de carros
        self.tempo_inicial = time.time()
        self.velocidades = []  # Lista para armazenar velocidades
        self.tf = 0  # Adicione essa linha para evitar o erro
        self.ti = 0  # Adicione essa linha para evitar o erro
        self.carro_parado = False  # Variável para rastrear se um carro está parado
        self.ti_luz_acessa = 0
        self.tf_luz_acessa = 0

        self.carros_passados_vermelho = 0
        self.sinal_vermelho = False
        self.infracao_sinal_vermelho = 0
        self.infracao_limite_velocidade = 0
        self.limite_velocidade = limite_velocidade

        if is_via_auxiliar:
            self.velocidade_maxima = 60  # Limite de velocidade da via auxiliar em km/h
        else:
            self.velocidade_maxima = 80  # Limite de velocidade da via principal em km/h

        GPIO.add_event_detect(pino_sensor, GPIO.BOTH, callback=self.sensores_callback)

    def sensores_callback(self, channel):
        global total_carros_passados  # Acessa a variável global
        if GPIO.input(self.pino_sensor):
            self.ti = time.time()
        else:
            self.tf = time.time()
            intervalo_tempo = self.tf - self.ti
            if 0.015 <= intervalo_tempo <= 0.3:
                distancia_carro_metros = 2
                distancia_carro_quilômetros = distancia_carro_metros / 1000  # Converter para quilômetros
                intervalo_tempo_horas = intervalo_tempo / 3600  # Converter para horas
                self.velocidade = distancia_carro_quilômetros / intervalo_tempo_horas
                self.carros_passados += 1  # Incrementa o contador de carros
                total_carros_passados += 1  # Incrementa o contador global de carros
                self.velocidades.append(self.velocidade)

                # Verifica se o carro está parado com base no intervalo de tempo
                if intervalo_tempo > 0.3:
                    self.carro_parado = True
                else:
                    self.carro_parado = False

                # Verifica se houve excesso de velocidade e registra a infração
                if not self.carro_parado and self.velocidade > self.limite_velocidade:
                    self.infracao_limite_velocidade += 1

                # Verifique se o sinal está vermelho e registra a infração de sinal vermelho
                if self.sinal_vermelho:
                    self.passagem_carro()

    def get_velocidade(self):
        return self.velocidade

    def get_carros_passados(self):
        return self.carros_passados

    def get_velocidade_media(self):
        if self.carros_passados > 0:
            return sum(self.velocidades) / self.carros_passados
        else:
            return 0

    def get_total_carros_passados(self):
        return total_carros_passados

    def get_carro_parado(self):
        return self.carro_parado

    def set_carro_passando(self):
        self.carro_parado = False

    def get_excesso_velocidade(self):
        return self.infracao_limite_velocidade
    
    def set_sinal_vermelho(self):
        self.sinal_vermelho = True

    def set_sinal_verde(self):
        self.sinal_vermelho = False

    def passagem_carro(self):
        if self.sinal_vermelho:
            self.carros_passados_vermelho += 1

    def get_infracoes_sinal_vermelho(self):
        return self.carros_passados_vermelho

    

"""
def main():
    sensor_pri_1 = sensor(0)  # Esquerda (pri 1)
    sensor_pri_2 = sensor(27)  # Direita (pri 2)
    sensor_aux_1 = sensor(26)  # Cima (aux1 1)
    sensor_aux_2 = sensor(22)  # Baixo (aux 2)

    while True:
        velocidade_pri_1 = sensor_pri_1.get_velocidade()
        velocidade_pri_2 = sensor_pri_2.get_velocidade()
        velocidade_aux_1 = sensor_aux_1.get_velocidade()
        velocidade_aux_2 = sensor_aux_2.get_velocidade()

        carros_passados_pri_1 = sensor_pri_1.get_carros_passados()
        carros_passados_pri_2 = sensor_pri_2.get_carros_passados()
        carros_passados_aux_1 = sensor_aux_1.get_carros_passados()
        carros_passados_aux_2 = sensor_aux_2.get_carros_passados()

        velocidade_media_pri_1 = sensor_pri_1.get_velocidade_media()
        velocidade_media_pri_2 = sensor_pri_2.get_velocidade_media()
        velocidade_media_aux_1 = sensor_aux_1.get_velocidade_media()
        velocidade_media_aux_2 = sensor_aux_2.get_velocidade_media()

        print("\n\n")
        print("\n---")
        print(f"Vel Principal 1 (esquerda) = {velocidade_pri_1:.2f} km/h")
        print(f"Vel Principal 2 (direita)  = {velocidade_pri_2:.2f} km/h")
        print(f"Vel Aux 1       (cima)     = {velocidade_aux_1:.2f} km/h")
        print(f"Vel Aux 2       (baixo)    = {velocidade_aux_2:.2f} km/h")
        print("\n---")
        print(f"Carros passados Principal 1 (esquerda) = {carros_passados_pri_1}")
        print(f"Carros passados Principal 2 (direita)  = {carros_passados_pri_2}")
        print(f"Carros passados Aux 1       (cima)     = {carros_passados_aux_1}")
        print(f"Carros passados Aux 2       (baixo)    = {carros_passados_aux_2}")
        print(f"Total de carros passados: {total_carros_passados}")
        print("\n---")
        print(f"Vel Média Principal 1 (esquerda) = {velocidade_media_pri_1:.2f} km/h")
        print(f"Vel Média Principal 2 (direita)   = {velocidade_media_pri_2:.2f} km/h")
        print(f"Vel Média Auxiliar 1  (cima)     = {velocidade_media_aux_1:.2f} km/h")
        print(f"Vel Média Auxiliar 2  (baixo)     = {velocidade_media_aux_2:.2f} km/h")
        print("\n---")
        print(f"Fluxo Principal (esquerda/direita) = {carros_passados_pri_1 + carros_passados_pri_2} carros/min")
        print(f"Fluxo Auxiliar  (cima/baixo)     = {carros_passados_aux_1 + carros_passados_aux_2} carros/min")

        time.sleep(2)  # Atualizar as informações a cada 2 segundos

if __name__ == "__main__":
    main()

"""