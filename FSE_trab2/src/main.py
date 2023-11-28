import logging
import log
from threading import Thread, Event
import signal
import sys
from time import sleep

logging.getLogger('').handlers.clear()
log.config_logging()

import cmds
import uart
import lcd
import gpio
import pid
import struct

pid_control = pid.PID()
pid_control.configura_constantes(Kp=0.1, Ki=0.05, Kd=0.01)
pid_control.atualiza_referencia(0.0)

controle = cmds.controle

exit_execution = Event()

def finaliza_programa(sig, frame):
    logging.info("Recebido sinal para finalizar o programa.")
    controle.stop_pwm()
    gpio.GPIO.cleanup()
    exit_execution.set()
    logging.info("Programa interrompido pelo usuário.")
    sys.exit(0)
    
try:
    # Iniciando as threads
    thread_apurar_lcd = Thread(target=cmds.apurar_lcd, args=(exit_execution,))
    thread_menu_elevador = Thread(target=cmds.menu_elevador, args=(exit_execution,))
    # thread_le_regs = Thread(target=cmds.le_regs)

    # Configurando as threads como daemon
    thread_apurar_lcd.daemon = True
    thread_menu_elevador.daemon = True
    # thread_le_regs.daemon = True

    # Configurando o tratamento de sinais para finalizar o programa
    signal.signal(signal.SIGINT, finaliza_programa)
    signal.signal(signal.SIGTERM, finaliza_programa)

    # Iniciando as threads
    thread_apurar_lcd.start()
    thread_menu_elevador.start()
    # thread_le_regs.start()

    # Aguardando as threads terminarem (se necessário)
    thread_apurar_lcd.join()
    thread_menu_elevador.join()
    # thread_le_regs.join()

except KeyboardInterrupt:
    logging.info("Programa interrompido pelo usuario")

finally:
    # Limpar configurações ao finalizar
    cmds.controle.stop_pwm()
    gpio.GPIO.cleanup()
