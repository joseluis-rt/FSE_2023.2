import logging

import serial
from time import sleep
import struct
import crc

uart0_filestream = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

if uart0_filestream == -1:
    logging.error("Não foi possível iniciar a UART.\n")
else:
    logging.info("UART inicializada!\n")

def envia_comando(comando, *args):
    msg = bytes(comando)

    for valor in args:
        if type(valor) == int:
            msg += struct.pack('<i', valor)
        elif type(valor) == float:
            msg += struct.pack('<f', valor)
        elif type(valor) == list:
            msg += bytes(valor)
        else:
            logging.warning(f"Tipo de valor não suportado: {type(valor)}")

    crc_calculado = crc.calcula_crc(msg, len(msg))
    mensagem_crc = msg + crc_calculado.to_bytes(2, 'little')
    uart0_filestream.write(mensagem_crc)

def recebe_resposta():
    if uart0_filestream.in_waiting >= 9:
        resposta = uart0_filestream.read(9)

        if len(resposta) != 9:
            logging.error("Erro de comunicação")
            return None

        crc_calculado = crc.calcula_crc(resposta, len(resposta) - 2)
        crc_recebido = struct.unpack('<H', resposta[-2:])[0]

        # logging.debug(f"Resposta recebida: {resposta}")
        # logging.debug(f"CRC calculado: {crc_calculado}")
        # logging.debug(f"CRC recebido: {crc_recebido}")

        cod = resposta[0:1]

        if crc_calculado == crc_recebido:

            if cod == b'\x03' or cod == b'\x06': # Encoder
                info = resposta[3:7]
                reg = info[-1]
                return reg
            elif cod == b'\x16': # PWM ou Temp
                info = resposta[3:7]
                temp = int.from_bytes(info, byteorder='big')
                return temp
            else: # Temp
                info = resposta[3:7]
                encoder = int.from_bytes(info, byteorder='little')
                return encoder
        else:
            # logging.error("Erro de CRC")
            return None

def envia_recebe(comando, *args):
    tentativas = 0

    uart0_filestream.flushInput()
    while True:
        envia_comando(comando, *args)
        sleep(0.05) 
        resposta = recebe_resposta()

        if resposta is not None:
            # logging.debug(f"Resposta recebida: {resposta}")
            return resposta

        # logging.debug(f"[{tentativas}] CRC não corresponde. Reenviando...")
        tentativas += 1 


# #import i2c_bmp280
# import i2c_bme280

# import log
# logging.getLogger('').handlers.clear()
# log.config_logging()

# # Trocar entre i2c_bmp280 ou i2c_bme280
# temperature = i2c_bme280.temp_ambiente()
# rounded_temperature = round(temperature, 2)

# cod = [0x01]  # (Endereço da ESP32) 
# id = [7, 8, 5, 8] # Matrícula

# #Mensagens
# le_encoder = [cod[0], 0x23, 0xC1, *id]
# envia_pwm = [cod[0], 0x16, 0xC2, *struct.pack("<i", 100), *id] 
# envia_temp = [cod[0], 0x16, 0xD1, *struct.pack('<f', temperature), *id]

# le_btnT = [cod[0], 0x03, 0x00, 1, *id]
# le_btn1_descer = [cod[0], 0x03, 0x01, 1, *id]
# le_btn1_subir = [cod[0], 0x03, 0x02, 1, *id]
# le_btn2_descer = [cod[0], 0x03, 0x03, 1, *id]
# le_btn2_subir = [cod[0], 0x03, 0x04, 1, *id]
# le_btn3 = [cod[0], 0x03, 0x05, 1, *id]
# le_btn_em = [cod[0], 0x03, 0x06, 1, *id]
# le_btnE_T = [cod[0], 0x03, 0x07, 1, *id]
# le_btnE_1 = [cod[0], 0x03, 0x08, 1, *id]
# le_btnE_2 = [cod[0], 0x03, 0x09, 1, *id]
# le_btnE_3 = [cod[0], 0x03, 0x0A, 1, *id]

# on = [1]
# off = [0]
# escr_btnT_off = [cod[0], 0x06, 0x00, 1, *off, *id]
# escr_btnT_on = [cod[0], 0x06, 0x00, 1, *on, *id]

# escr_btn1_descer_off = [cod[0], 0x06, 0x01, 1, *off, *id]
# escr_btn1_descer_on = [cod[0], 0x06, 0x01, 1, *on, *id]

# escr_btn1_subir_off = [cod[0], 0x06, 0x02, 1, *off, *id]
# escr_btn1_subir_on = [cod[0], 0x06, 0x02, 1, *on, *id]

# escr_btn2_descer_off = [cod[0], 0x06, 0x03, 1, *off, *id]
# escr_btn2_descer_on = [cod[0], 0x06, 0x03, 1, *on, *id]

# escr_btn2_subir_off = [cod[0], 0x06, 0x04, 1, *off, *id]
# escr_btn2_subir_on = [cod[0], 0x06, 0x04, 1, *on, *id]

# escr_btn3_off = [cod[0], 0x06, 0x05, 1, *off, *id]
# escr_btn3_on = [cod[0], 0x06, 0x05, 1, *on, *id]

# escr_btn_em_off = [cod[0], 0x06, 0x06, 1, *off, *id]
# escr_btn_em_on = [cod[0], 0x06, 0x06, 1, *on, *id]

# escr_btnE_T_off = [cod[0], 0x06, 0x07, 1, *off, *id]
# escr_btnE_T_on = [cod[0], 0x06, 0x07, 1, *on, *id]

# escr_btnE_1_off = [cod[0], 0x06, 0x08, 1, *off, *id]
# escr_btnE_1_on = [cod[0], 0x06, 0x08, 1, *on, *id]

# escr_btnE_2_off = [cod[0], 0x06, 0x09, 1, *off, *id]
# escr_btnE_2_on = [cod[0], 0x06, 0x09, 1, *on, *id]

# escr_btnE_3_off = [cod[0], 0x06, 0x0A, 1, *off, *id]
# escr_btnE_3_on = [cod[0], 0x06, 0x0A, 1, *on, *id]

# def le_regs():
#     btnT = envia_recebe(le_btnT)
#     btn1_descer = envia_recebe(le_btn1_descer)
#     btn1_subir = envia_recebe(le_btn1_subir)
#     btn2_descer = envia_recebe(le_btn2_descer)
#     btn2_subir = envia_recebe(le_btn2_subir)
#     btn3 = envia_recebe(le_btn3)
    
#     btn_em = envia_recebe(le_btn_em)
#     btnE_T = envia_recebe(le_btnE_T)
#     btnE_1 = envia_recebe(le_btnE_1)
#     btnE_2 = envia_recebe(le_btnE_2)
#     btnE_3 = envia_recebe(le_btnE_3)

#     print("\n  Andares  | Elevador")
#     print(f"3.......:{btn3} | E_3...:{btnE_3}")
#     print(f"2_subir.:{btn2_subir} | E_2...:{btnE_2}")
#     print(f"2_descer:{btn2_descer} | E_1...:{btnE_1}")
#     print(f"1_subir.:{btn1_subir} | E_T...:{btnE_T}", )
#     print(f"1_descer:{btn1_descer} | Em....:{btn_em}")
#     print(f"T.......:{btnT} | \n")

# def escr_regs_off():
#     envia_recebe(escr_btnT_off)
#     envia_recebe(escr_btn1_descer_off)
#     envia_recebe(escr_btn1_subir_off)
#     envia_recebe(escr_btn2_descer_off)
#     envia_recebe(escr_btn2_subir_off)
#     envia_recebe(escr_btn3_off)
#     envia_recebe(escr_btn_em_off)
#     envia_recebe(escr_btnE_T_off)
#     envia_recebe(escr_btnE_1_off)
#     envia_recebe(escr_btnE_2_off)
#     envia_recebe(escr_btnE_3_off)

# def escr_regs_on():
#     envia_recebe(escr_btnT_on)
#     envia_recebe(escr_btn1_descer_on)
#     envia_recebe(escr_btn1_subir_on)
#     envia_recebe(escr_btn2_descer_on)
#     envia_recebe(escr_btn2_subir_on)
#     envia_recebe(escr_btn3_on)
#     envia_recebe(escr_btn_em_on)
#     envia_recebe(escr_btnE_T_on)
#     envia_recebe(escr_btnE_1_on)
#     envia_recebe(escr_btnE_2_on)
#     envia_recebe(escr_btnE_3_on)

# try:
#     valor_encoder = envia_recebe(le_encoder)
#     logging.info("Leitura completo!")
#     logging.info(f"Encoder: {valor_encoder}")
#     sleep(3)

#     valor_pwm = envia_recebe(envia_pwm)
#     logging.info("Envio completo!")
#     logging.info(f"Pwm: {valor_pwm}")
#     sleep(3)

#     valor_temp = envia_recebe(envia_temp)
#     logging.info("Envio completo!")
#     logging.info(f"Temp: {valor_temp}")
#     sleep(3)
    
#     # escr_regs_on()

#     le_regs()

# except KeyboardInterrupt:
#     logging.info("Programa interrompido pelo usuario")

