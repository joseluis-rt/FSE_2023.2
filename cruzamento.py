from semaforo import semaforo
from botao_pedestre import botao_pedestre
from sensor import sensor
from buzzer import Buzzer

from time import sleep
import os

class cruzamento:
    def __init__(self, id, semaforo_pri_pino1, semaforo_pri_pino2,  
                    semaforo_aux_pino1, semaforo_aux_pino2, 
                    botao1, botao2,
                    sensor_aux_a, sensor_aux_b,
                    sensor_pri_a, sensor_pri_b,
                    buzzer):
        
        self.id = id
        self.contador_segundos = 1 # Inicializa o contador de segundos com 1
        self.tempo_estado = 0
        self.estado = 0

        self.smf_principal = semaforo(n_semaforo=1, pino1=semaforo_pri_pino1, pino2=semaforo_pri_pino2)
        self.smf_auxiliar = semaforo(n_semaforo=2, pino1=semaforo_aux_pino1, pino2=semaforo_aux_pino2)

        self.is_botao_pedestre = False
        self.botao_pedestre1 = botao_pedestre(botao1)
        self.botao_pedestre2 = botao_pedestre(botao2)

        self.is_carro_esperando_auxiliar = False
        self.sensor_aux_1 = sensor(sensor_aux_a, limite_velocidade=60, is_via_auxiliar=True)
        self.sensor_aux_2 = sensor(sensor_aux_b, limite_velocidade=60, is_via_auxiliar=True)

        self.is_carro_esperando_principal = False
        self.sensor_pri_1 = sensor(sensor_pri_a, limite_velocidade=80)
        self.sensor_pri_2 = sensor(sensor_pri_b, limite_velocidade=80)

        self.infracoes_sinal_vermelho = 0
        self.infracoes_excesso_velocidade = 0

        self.buzzer = Buzzer(buzzer)


    def controle_estados(self):
        if(self.estado == 0):
            #As duas vias fechadas
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias principais self.infracoes_sinal_vermelho +=1
            self.sensor_pri_1.set_infracoes_sinal_vermelho()
            self.sensor_pri_2.set_infracoes_sinal_vermelho()
            self.smf_principal.pare()
            self.smf_auxiliar.atencao()
            self.buzzer.buzzer_on()  # Ligar o buzzer
            self.estado = 1
        elif(self.estado == 1):
            # Via Auxiliar fechada e via Principal aberta
            self.buzzer.buzzer_off()  # Desligar o buzzer
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias auxiliares self.infracoes_sinal_vermelho +=1
            self.sensor_aux_1.set_infracoes_sinal_vermelho()
            self.sensor_aux_2.set_infracoes_sinal_vermelho()
            if(self.tempo_estado >= 10 and self.is_carro_esperando_auxiliar == True):
                self.estado = 2
                self.tempo_estado = 0
            elif(self.tempo_estado >= 20):
                self.estado = 2
                self.tempo_estado = 0
            else:
                self.smf_principal.passe()
                self.smf_auxiliar.pare()
                self.tempo_estado +=1
        elif(self.estado == 2):
            # Via Principal em atenção
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias auxiliares self.infracoes_sinal_vermelho +=1
            self.sensor_aux_1.set_infracoes_sinal_vermelho()
            self.sensor_aux_2.set_infracoes_sinal_vermelho()
            self.smf_principal.atencao()
            self.smf_auxiliar.pare()
            self.buzzer.buzzer_on()  # Ligar o buzzer
            self.estado = 3
        elif(self.estado == 3):
            # As duas vias fechadas
            self.buzzer.buzzer_off()  # Desligar o buzzer
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias principais self.infracoes_sinal_vermelho +=1
            self.sensor_pri_1.set_infracoes_sinal_vermelho()
            self.sensor_pri_2.set_infracoes_sinal_vermelho()
            self.smf_principal.pare()
            self.smf_auxiliar.passe()
            self.estado = 4
        elif(self.estado == 4):
            # Via Auxiliar aberta e via Principal fechada
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias principais self.infracoes_sinal_vermelho +=1
            self.sensor_pri_1.set_infracoes_sinal_vermelho()
            self.sensor_pri_2.set_infracoes_sinal_vermelho()
            if(self.tempo_estado >= 5 and (self.is_botao_pedestre or self.is_carro_esperando_principal)):
                self.estado = 5
                self.tempo_estado = 0
            elif(self.tempo_estado >= 10):
                self.estado = 5
                self.tempo_estado = 0
            else:
                self.smf_principal.pare()
                self.smf_auxiliar.passe()
                self.tempo_estado +=1
        elif(self.estado == 5):
            # Via auxiliar em atenção
            self.verifica_pedestre_esperando()
            self.verifica_carro_esperando_principal()
            self.verifica_carro_esperando_auxiliar()
            #se passar carro nas vias principais self.infracoes_sinal_vermelho +=1
            self.sensor_pri_1.set_infracoes_sinal_vermelho()
            self.sensor_pri_2.set_infracoes_sinal_vermelho()
            self.smf_principal.pare()
            self.smf_auxiliar.atencao()
            self.buzzer.buzzer_on()  # Ligar o buzzer
            self.estado = 0

        elif(self.estado == 6):
            self.smf_principal.amarelo()
            self.smf_auxiliar.amarelo()
            sleep(1)
            self.smf_principal.desligado()
            self.smf_auxiliar.desligado()

        elif(self.estado == 7):
            #se passar carro nas vias auxiliares self.infracoes_sinal_vermelho +=1
            self.sensor_aux_1.set_infracoes_sinal_vermelho()
            self.sensor_aux_2.set_infracoes_sinal_vermelho()
            self.smf_principal.passe()
            self.smf_auxiliar.pare()

        sleep(1)
        self.contador_segundos+=1

        self.infracoes_sinal_vermelho = self.sensor_aux_1.get_infracoes_sinal_vermelho() + self.sensor_aux_2.get_infracoes_sinal_vermelho() + self.sensor_pri_1.get_infracoes_sinal_vermelho() + self.sensor_pri_2.get_infracoes_sinal_vermelho()

        self.infracoes_excesso_velocidade = self.sensor_aux_1.get_excesso_velocidade()+self.sensor_aux_2.get_excesso_velocidade()+self.sensor_pri_1.get_excesso_velocidade()+self.sensor_pri_2.get_excesso_velocidade()


    def ativa_noturno(self):
        self.estado = 6
  
    def ativa_emergencia(self):
        self.estado = 7

    def desativa_noturno_emergencia(self):
        if(self.estado == 6 or self.estado == 7):
            self.estado = 0
  
    def modo_pedestre(self):
        if(self.estado != 1):
            self.is_botao_pedestre = True
        else:
            self.is_botao_pedestre = False
      
    def verifica_pedestre_esperando(self):
        if(self.estado != 1 and (self.botao_pedestre1.get_pedestre_esperando() or self.botao_pedestre2.get_pedestre_esperando())):
            self.is_botao_pedestre = True
        else:
            self.botao_pedestre1.set_pedestre_passando()
            self.botao_pedestre2.set_pedestre_passando()
            self.is_botao_pedestre = False

    def verifica_carro_esperando_principal(self):
        if(self.estado != 1 and (self.sensor_pri_1.get_carro_parado() or self.sensor_pri_2.get_carro_parado())):
            self.is_carro_esperando_principal = True
        else:
            self.sensor_pri_1.set_carro_passando()
            self.sensor_pri_2.set_carro_passando()
            self.is_carro_esperando_principal = False

    def verifica_carro_esperando_auxiliar(self):
        if(self.estado != 1 and (self.sensor_aux_1.get_carro_parado() or self.sensor_aux_2.get_carro_parado())):
            self.is_carro_esperando_auxiliar = True
        else:
            self.sensor_aux_1.set_carro_passando()
            self.sensor_aux_2.set_carro_passando()
            self.is_carro_esperando_auxiliar = False

    def mostra_informacoes(self):
        print('')
        print(f'------------CRUZAMENTO {self.id}--------------')
        print("--------FLUXO DE TRANSITO--------")
        print(f'Qtd (Carros/min) →: {int((self.sensor_pri_1.get_carros_passados()/self.contador_segundos)*60)}')
        print(f'Qtd (Carros/min) ←: {int((self.sensor_pri_2.get_carros_passados()/self.contador_segundos)*60)}')
        print(f'Qtd (Carros/min) ↓: {int((self.sensor_aux_1.get_carros_passados()/self.contador_segundos)*60)}')
        print(f'Qtd (Carros/min) ↑: {int((self.sensor_aux_2.get_carros_passados()/self.contador_segundos)*60)}')
        print(f'Ttl (Carros/min)  : {int((self.sensor_pri_1.get_total_carros_passados() / self.contador_segundos) * 60)}')
        #print("--------CARRO PARADO--------")
        #print(f'carro parado na →: {"Sim" if self.sensor_pri_1.get_carro_parado() else "Nao"}')
        #print(f'carro parado na ←: {"Sim" if self.sensor_pri_2.get_carro_parado() else "Nao"}')
        #print(f'carro parado na ↓: {"Sim" if self.sensor_aux_1.get_carro_parado() else "Nao"}')
        #print(f'carro parado na ↑: {"Sim" if self.sensor_aux_2.get_carro_parado() else "Nao"}')
        print("--------VELOCIDADE MEDIA DA VIA--------")
        print(f'Vel Media (km/h) →: {self.sensor_pri_1.get_velocidade_media():.2f}')
        print(f'Vel Media (km/h) ←: {self.sensor_pri_2.get_velocidade_media():.2f}')
        print(f'Vel Media (km/h) ↓: {self.sensor_aux_1.get_velocidade_media():.2f}')
        print(f'Vel Media (km/h) ↑: {self.sensor_aux_2.get_velocidade_media():.2f}')
        print('')
        print("------------INFRACOES-------------")
        print(f'Qtd Infracoes (sinal vermelho)       : {self.infracoes_sinal_vermelho}')
        print(f'Qtd Infracoes (excesso de velocidade): {self.infracoes_excesso_velocidade}')
        print('')
