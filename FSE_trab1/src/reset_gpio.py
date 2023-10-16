import RPi.GPIO as GPIO
from time import sleep

# Define o padrao de numeracao das portas como BCM
# A outra opcap e GPIO.BOARD para usar o numero dos pinos fisicos da placa
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

output_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 0, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21]

for pin in output_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)