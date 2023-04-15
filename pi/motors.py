
import RPi.GPIO as GPIO
from time import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motor_pins = {'rotation_1': 4,
              'rotation_2': 18,
              'pwm1': 17,
              'pwm2': 27,
              'pwm3': 22,
              'pwm4': 24}


for pin in motor_pins:
    GPIO.setup(motor_pins[pin], GPIO.OUT)
for pin in ['pwm1', 'pwm2', 'pwm3', 'pwm4']:
    GPIO.output(motor_pins[pin], False)


def set_rotation(direction='counter_clockwise'):
    if direction == 'clockwise':
        GPIO.output(motor_pins['rotation_1'], True)
        GPIO.output(motor_pins['rotation_2'], False)
    elif direction == 'counter_clockwise':
        GPIO.output(motor_pins['rotation_1'], False)
        GPIO.output(motor_pins['rotation_2'], True)


def run_motor(motor, duration, direction='counter_clockwise'):
    """
    motor: int
        Which motor to run? 1 -> Motor 1, 2 -> Motor 2, 3 -> Motor 3, 4 -> Motor 4
    duration: float
        Time in seconds to run the motor
    """

    start_time = time()
    while (time() - start_time) < duration:
        set_rotation(direction)
        if motor == 1:
            GPIO.output(motor_pins['pwm1'], True)
        elif motor == 2:
            GPIO.output(motor_pins['pwm2'], True)
        elif motor == 3:
            GPIO.output(motor_pins['pwm3'], True)
        elif motor == 4:
            GPIO.output(motor_pins['pwm4'], True)

    for pin in ['pwm1', 'pwm2', 'pwm3', 'pwm4']:
        GPIO.output(motor_pins[pin], False)

    # GPIO.cleanup(list(motor_pins.values()))


# Need to do this again because the earlier scope doesn't remain valid.
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(motor_pins[pin], GPIO.OUT)
for pin in ['pwm1', 'pwm2', 'pwm3', 'pwm4']:
    GPIO.output(motor_pins[pin], False)

# exit()

if __name__ == '__main__':

    run_motor(motor=3, duration=0.2)

    # Need to do this again because the earlier scope doesn't remain valid.
    GPIO.setmode(GPIO.BCM)
    for pin in motor_pins:
        GPIO.setup(motor_pins[pin], GPIO.OUT)
    for pin in ['pwm1', 'pwm2', 'pwm3', 'pwm4']:
        GPIO.output(motor_pins[pin], False)
