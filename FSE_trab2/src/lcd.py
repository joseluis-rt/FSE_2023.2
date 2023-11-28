import smbus
from time import sleep

# Define alguns parâmetros do dispositivo
I2C_ADDR = 0x27  # Endereço do dispositivo I2C

# Define algumas constantes do dispositivo
LCD_CHR = 1  # Modo - Envio de dados
LCD_CMD = 0  # Modo - Envio de comando
LCD_BACKLIGHT = 0x08  # Ligado
# LCD_BACKLIGHT = 0x00  # Desligado

LINE1 = 0x80  # 1ª linha
LINE2 = 0xC0  # 2ª linha

ENABLE = 0b00000100  # Bit de habilitação

# Inicializa a comunicação I2C
bus = smbus.SMBus(1)

def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Inicializa
    lcd_byte(0x32, LCD_CMD)  # Inicializa
    lcd_byte(0x06, LCD_CMD)  # Direção do movimento do cursor
    lcd_byte(0x0C, LCD_CMD)  # 0x0F Ligado, Sem piscar
    lcd_byte(0x28, LCD_CMD)  # Comprimento dos dados, número de linhas, tamanho da fonte
    lcd_byte(0x01, LCD_CMD)  # Limpar o display
    sleep(0.0005)

def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Alternar o pino de habilitação no display LCD
    sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    sleep(0.0005)

def lcdLoc(line):
    lcd_byte(line, LCD_CMD)

def ClrLcd():
    lcd_byte(0x01, LCD_CMD)
    lcd_byte(0x02, LCD_CMD)

def typeChar(val):
    lcd_byte(val, LCD_CHR)

def typeln(s):
    for char in s:
        lcd_byte(ord(char), LCD_CHR)
