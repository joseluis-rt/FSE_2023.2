import logging

import uart
import lcd
import gpio
#import i2c_bmp280
import i2c_bme280

import struct
from time import sleep

cod = [0x01]  # (Endereço da ESP32) 
id = [7, 8, 5, 8] # Matrícula

controle = gpio.GPIOController()

pwm_global = 40

# Trocar entre i2c_bmp280 ou i2c_bme280
temperature = i2c_bme280.temp_ambiente()
rounded_temperature = round(temperature, 2)

#Mensagens
le_encoder = [cod[0], 0x23, 0xC1, *id]
envia_pwm = [cod[0], 0x16, 0xC2, *struct.pack("<i", pwm_global), *id] 
envia_temp = [cod[0], 0x16, 0xD1, *struct.pack('<f', temperature), *id]

le_btnT = [cod[0], 0x03, 0x00, 1, *id]
le_btn1_descer = [cod[0], 0x03, 0x01, 1, *id]
le_btn1_subir = [cod[0], 0x03, 0x02, 1, *id]
le_btn2_descer = [cod[0], 0x03, 0x03, 1, *id]
le_btn2_subir = [cod[0], 0x03, 0x04, 1, *id]
le_btn3 = [cod[0], 0x03, 0x05, 1, *id]
le_btn_em = [cod[0], 0x03, 0x06, 1, *id]
le_btnE_T = [cod[0], 0x03, 0x07, 1, *id]
le_btnE_1 = [cod[0], 0x03, 0x08, 1, *id]
le_btnE_2 = [cod[0], 0x03, 0x09, 1, *id]
le_btnE_3 = [cod[0], 0x03, 0x0A, 1, *id]

on = [1]
off = [0]
escr_btnT_off = [cod[0], 0x06, 0x00, 1, *off, *id]
escr_btnT_on = [cod[0], 0x06, 0x00, 1, *on, *id]

escr_btn1_descer_off = [cod[0], 0x06, 0x01, 1, *off, *id]
escr_btn1_descer_on = [cod[0], 0x06, 0x01, 1, *on, *id]

escr_btn1_subir_off = [cod[0], 0x06, 0x02, 1, *off, *id]
escr_btn1_subir_on = [cod[0], 0x06, 0x02, 1, *on, *id]

escr_btn2_descer_off = [cod[0], 0x06, 0x03, 1, *off, *id]
escr_btn2_descer_on = [cod[0], 0x06, 0x03, 1, *on, *id]

escr_btn2_subir_off = [cod[0], 0x06, 0x04, 1, *off, *id]
escr_btn2_subir_on = [cod[0], 0x06, 0x04, 1, *on, *id]

escr_btn3_off = [cod[0], 0x06, 0x05, 1, *off, *id]
escr_btn3_on = [cod[0], 0x06, 0x05, 1, *on, *id]

escr_btn_em_off = [cod[0], 0x06, 0x06, 1, *off, *id]
escr_btn_em_on = [cod[0], 0x06, 0x06, 1, *on, *id]

escr_btnE_T_off = [cod[0], 0x06, 0x07, 1, *off, *id]
escr_btnE_T_on = [cod[0], 0x06, 0x07, 1, *on, *id]

escr_btnE_1_off = [cod[0], 0x06, 0x08, 1, *off, *id]
escr_btnE_1_on = [cod[0], 0x06, 0x08, 1, *on, *id]

escr_btnE_2_off = [cod[0], 0x06, 0x09, 1, *off, *id]
escr_btnE_2_on = [cod[0], 0x06, 0x09, 1, *on, *id]

escr_btnE_3_off = [cod[0], 0x06, 0x0A, 1, *off, *id]
escr_btnE_3_on = [cod[0], 0x06, 0x0A, 1, *on, *id]

def menu_elevador(exit_event):
    while not exit_event.is_set():
        logging.info('Descendo o elevador...')
        controle.desce_tudo()
        valor_encoder = apurar_encoder()
        logging.info(f'Encoder: {valor_encoder}')

        logging.info('Reconhecendo andares...')
        controle.reconhece_andares()

        logging.info('Andares reconhecidos')

        logging.info('Indo para 1o Andar')
        controle.ir_para_andar(1)
        logging.info('Parou 1o Andar')
        sleep(5)

        logging.info('Indo para Terreo')
        controle.ir_para_andar(0)
        logging.info('Parou Terreo')
        sleep(5)


def apurar_lcd(exit_event):
    lcd.ClrLcd
    while not exit_event.is_set():
        temperature = i2c_bme280.temp_ambiente()
        lcd_temp = round(temperature, 2)

        atualiza_temp = [cod[0], 0x16, 0xD1, *struct.pack('<f', temperature), *id]
        uart.envia_recebe(atualiza_temp)

        lcd.lcd_init()
        lcd.lcdLoc(lcd.LINE1)
        lcd.typeln(f"{controle.status} : {controle.nome_andar}")
        lcd.lcdLoc(lcd.LINE2)
        lcd.typeln(f"Temp: {lcd_temp} C")
        lcd.ClrLcd
        sleep(0.2)


def apurar_encoder():
    valor = uart.envia_recebe(le_encoder)
    return valor

def apurar_pwm():
    uart.envia_recebe(envia_pwm)
    return 

def apurar_temp():
    valor_temp = uart.envia_recebe(envia_temp)
    return valor_temp

def le_regs():
    while True:
        btnT = uart.envia_recebe(le_btnT)
        btn1_descer = uart.envia_recebe(le_btn1_descer)
        btn1_subir = uart.envia_recebe(le_btn1_subir)
        btn2_descer = uart.envia_recebe(le_btn2_descer)
        btn2_subir = uart.envia_recebe(le_btn2_subir)
        btn3 = uart.envia_recebe(le_btn3)
        
        btn_em = uart.envia_recebe(le_btn_em)
        btnE_T = uart.envia_recebe(le_btnE_T)
        btnE_1 = uart.envia_recebe(le_btnE_1)
        btnE_2 = uart.envia_recebe(le_btnE_2)
        btnE_3 = uart.envia_recebe(le_btnE_3)

        print("\n  Andares  | Elevador")
        print(f"3.......:{btn3} | E_3...:{btnE_3}")
        print(f"2_subir.:{btn2_subir} | E_2...:{btnE_2}")
        print(f"2_descer:{btn2_descer} | E_1...:{btnE_1}")
        print(f"1_subir.:{btn1_subir} | E_T...:{btnE_T}", )
        print(f"1_descer:{btn1_descer} | Em....:{btn_em}")
        print(f"T.......:{btnT} | \n")

def escr_regs_off():
    uart.envia_recebe(escr_btnT_off)
    uart.envia_recebe(escr_btn1_descer_off)
    uart.envia_recebe(escr_btn1_subir_off)
    uart.envia_recebe(escr_btn2_descer_off)
    uart.envia_recebe(escr_btn2_subir_off)
    uart.envia_recebe(escr_btn3_off)
    uart.envia_recebe(escr_btn_em_off)
    uart.envia_recebe(escr_btnE_T_off)
    uart.envia_recebe(escr_btnE_1_off)
    uart.envia_recebe(escr_btnE_2_off)
    uart.envia_recebe(escr_btnE_3_off)

def escr_regs_on():
    uart.envia_recebe(escr_btnT_on)
    uart.envia_recebe(escr_btn1_descer_on)
    uart.envia_recebe(escr_btn1_subir_on)
    uart.envia_recebe(escr_btn2_descer_on)
    uart.envia_recebe(escr_btn2_subir_on)
    uart.envia_recebe(escr_btn3_on)
    uart.envia_recebe(escr_btn_em_on)
    uart.envia_recebe(escr_btnE_T_on)
    uart.envia_recebe(escr_btnE_1_on)
    uart.envia_recebe(escr_btnE_2_on)
    uart.envia_recebe(escr_btnE_3_on)

# valor_escr_btn = uart.envia_recebe(escr_btn3_on)
# if valor_escr_btn is not None:
#     logging.info(f"\nEscreve btn: {valor_escr_btn}")
# else:
#     logging.info("\nFalha ao obter o valor do botão escrito")