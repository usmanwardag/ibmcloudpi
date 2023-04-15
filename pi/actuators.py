
import RPi.GPIO as GPIO
from time import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

actuator_pins = {'light': 21,
                 'humidifier': 20,
                 'fan': 16}

for pin in actuator_pins:
    GPIO.setup(actuator_pins[pin], GPIO.OUT)


def set_light(status):
    # Light is controlled by mechanical relay (1). 0 -> On, 1 -> Off
    if status == True:
        GPIO.output(actuator_pins['light'], False)
    elif status == False:
        GPIO.output(actuator_pins['light'], True)


def set_humidifier(status):
    # Humidifier is controlled by SSR-1. 1 -> On, 0 -> Off
    GPIO.output(actuator_pins['humidifier'], status)


def set_fan(status):
    # Fan is controlled by SSR2-2. 1 -> On, 0 -> Off
    GPIO.output(actuator_pins['fan'], status)


if __name__ == '__main__':

    # t = time()
    # while (time() - t) < 5:
    #     set_humidifier(True)
    # set_humidifier(False)

    # t = time()
    # while (time() - t) < 5:
    #     set_fan(True)
    # set_fan(False)

    set_light(True)
