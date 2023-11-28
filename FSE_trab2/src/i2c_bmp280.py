import smbus2
from bmp280 import BMP280  # Importa a classe BMP280 do módulo bmp280
from time import sleep

# Cria uma instância da classe BMP280
bmp280 = BMP280()

def temp_ambiente():
    temperature = bmp280.get_temperature()
    return temperature

"""
# Exemplo de uso
try:
    while True:
        temperature = temp_ambiente()
        temperature_formatada = round(temperature, 2)
        print(f"temperature ambiente: {temperature_formatada} °C")
        sleep(1)

except KeyboardInterrupt:
    print("\n\nPrograma interrompido pelo usuário.")
"""