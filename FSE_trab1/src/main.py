import RPi.GPIO as GPIO
from time import sleep
from cruzamento import cruzamento
import signal
import sys
from threading import Thread, Event
import os

# Defina o modo de numeração de pinos como BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

exit_execution = Event()

if __name__ == "__main__":

    cruzamento1 = cruzamento(
                        id = 1,
                        semaforo_pri_pino1 = 9,
                        semaforo_pri_pino2 = 11,
                        semaforo_aux_pino1 = 5,
                        semaforo_aux_pino2 = 6,
                        botao1 = 13,
                        botao2 = 19,
                        sensor_aux_a = 26, 
                        sensor_aux_b = 22,
                        sensor_pri_a = 0, 
                        sensor_pri_b = 27,
                        buzzer = 17)
    
    cruzamento2 = cruzamento(
                        id = 2,
                        semaforo_pri_pino1 = 10,
                        semaforo_pri_pino2 = 8,
                        semaforo_aux_pino1 = 1,
                        semaforo_aux_pino2 = 18,
                        botao1 = 23,
                        botao2 = 24,
                        sensor_aux_a = 25, 
                        sensor_aux_b = 12,
                        sensor_pri_a = 16, 
                        sensor_pri_b = 20,
                        buzzer = 21)
    
    def executa_cruzamento1():
        while True:
            if exit_execution.is_set():
                cruzamento1.smf_principal.desliga_semaforo()
                cruzamento1.smf_auxiliar.desliga_semaforo()
                break
            cruzamento1.controle_estados()

    def executa_cruzamento2():
        while True:
            if exit_execution.is_set():
                cruzamento2.smf_principal.desliga_semaforo()
                cruzamento2.smf_auxiliar.desliga_semaforo()
                break
            cruzamento2.controle_estados()

    def modifica_modo():
        while True:
            if exit_execution.is_set():
                break
            else:
                modo = input('')
                if modo == 'N' or modo == 'n':  # Troque | por or e use == em vez de |
                    cruzamento1.ativa_noturno()
                    cruzamento2.ativa_noturno()
                elif modo == 'E' or modo == 'e':  # Troque | por or e use == em vez de |
                    cruzamento1.ativa_emergencia()
                    cruzamento2.ativa_emergencia()
                elif modo == 'X' or modo == 'x':  # Troque | por or e use == em vez de |
                    cruzamento1.desativa_noturno_emergencia()
                    cruzamento2.desativa_noturno_emergencia()

    def mostra_info():
        while True:
            if exit_execution.is_set():
                break
            else:
                sleep(2)
                os.system('clear')
                print('Digite N para o modo NOTURNO, E para o o modo EMERGENCIA" e X para desativa-los')
                cruzamento1.mostra_informacoes()
                cruzamento2.mostra_informacoes()
    
    def finaliza_programa(sig, frama):
        exit_execution.is_set()
        print("Até mais ...")
        sleep(2)
        sys.exit(0)

    tcruz1 = Thread(target=executa_cruzamento1)
    tcruz2 = Thread(target=executa_cruzamento2)
    modos = Thread(target=modifica_modo)
    informacoes = Thread(target=mostra_info)

    tcruz1.daemon = True
    tcruz2.daemon = True
    modos.daemon = True
    informacoes.daemon = True

    signal.signal(signal.SIGINT, finaliza_programa)
    signal.signal(signal.SIGTERM, finaliza_programa)

    tcruz1.start()
    tcruz2.start()
    informacoes.start()
    modos.start()

    tcruz1.join()
    tcruz2.join()
    informacoes.join()
    modos.join()

