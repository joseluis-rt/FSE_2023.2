import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def buzzer_on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def buzzer_off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
        
"""
if __name__ == "__main__":
    buzzer1 = Buzzer(17)

    try:
        while True:
            buzzer1.buzzer_on()
            time.sleep(1)
            buzzer1.buzzer_off()
            time.sleep(1)
    except KeyboardInterrupt:
        buzzer1.cleanup()
"""