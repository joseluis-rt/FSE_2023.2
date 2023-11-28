import smbus2
import bme280 
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def temp_ambiente():
    bme280_data = bme280.sample(bus,address)
    temp_ambiente = bme280_data.temperature
    return temp_ambiente

"""
# Exemplo de uso
try:
    while True:
        temperatura = temp_ambiente()
        temperatura_formatada = round(temperatura, 2)
        print(f"Temperatura ambiente: {temperatura_formatada} °C")
        sleep(1)

except KeyboardInterrupt:
    print("\n\nPrograma interrompido pelo usuário.")
"""