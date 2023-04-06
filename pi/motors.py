
import json
import RPi.GPIO as GPIO 
from time import time, sleep
from read_ph import get_ph 

GPIO.setwarnings(False)

rotation_1_pin = 7
rotation_2_pin = 12
pwm_motor1_pin = 11
pwm_motor2_pin = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(rotation_1_pin, GPIO.OUT)
GPIO.setup(rotation_2_pin, GPIO.OUT)
GPIO.setup(pwm_motor1_pin, GPIO.OUT)
GPIO.setup(pwm_motor2_pin, GPIO.OUT)

GPIO.output(pwm_motor1_pin, False)
GPIO.output(pwm_motor2_pin, False)


def set_rotation(direction='counter_clockwise'):
    if direction == 'clockwise':
        GPIO.output(rotation_1_pin, True)    
        GPIO.output(rotation_2_pin, False)
    elif direction == 'counter_clockwise':
        GPIO.output(rotation_1_pin, False)
        GPIO.output(rotation_2_pin, True)


def run_motor(motor, duration, direction='counter_clockwise'):
    """
    motor: int
        Which motor to run? 1 -> Motor 1, 2 -> Motor 2
    duration: float
        Time in seconds to run the motor
    """

    start_time = time()
    while (time() - start_time) < duration: 
        set_rotation(direction)
        if motor == 1:
            GPIO.output(pwm_motor1_pin, True)
        elif motor == 2:
            GPIO.output(pwm_motor2_pin, True)

    GPIO.output(pwm_motor1_pin, False)
    GPIO.output(pwm_motor2_pin, False)
    GPIO.cleanup()


def adjust_ph():
    
    # Motor 1 -> Acid, Motor 2 -> Base

    while True:

        # Read the latest config variables
        with open('config.json') as f:
            config = json.load(f)

            DESIRED_PH_LOWER = float(config['DESIRED_PH_LOWER'])
            DESIRED_PH_UPPER = float(config['DESIRED_PH_UPPER'])
            WAIT_TIME = float(config['WAIT_TIME'])
            PUMP_DURATION = float(config['PUMP_DURATION'])

        config['RUNNING'] = 'T'

        print(f'Lower pH Bound: {DESIRED_PH_LOWER}, Upper pH Bound: {DESIRED_PH_UPPER}, Wait: {WAIT_TIME}s, Pump Duration: {PUMP_DURATION}')

        _, ph = get_ph()
        print(f'Current PH: {ph}')

        if ph > DESIRED_PH_LOWER and ph < DESIRED_PH_UPPER:
            print('PH is within desired limits.')
            break

        elif ph < DESIRED_PH_LOWER:
            # Run motor 2, which controls base
            print('Running motor 2, which controls base (to increase pH).')
            run_motor(motor=2, duration=PUMP_DURATION)

        elif ph > DESIRED_PH_UPPER:
            # Run motor 1, which controls base
            print('Running motor 1, which controls acid (to decrease pH).')
            run_motor(motor=1, duration=PUMP_DURATION)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(rotation_1_pin, GPIO.OUT)
        GPIO.setup(rotation_2_pin, GPIO.OUT)
        GPIO.setup(pwm_motor1_pin, GPIO.OUT)
        GPIO.setup(pwm_motor2_pin, GPIO.OUT)
        GPIO.output(pwm_motor1_pin, False)
        GPIO.output(pwm_motor2_pin, False)

        with open("config.json", "w") as f:
            json.dump(config, f)

        # Wait for 30 seconds for readings to become stable
        print(f'Sleeping for {WAIT_TIME} seconds')
        sleep(WAIT_TIME)

    config['RUNNING'] = 'F'    
    with open("config.json", "w") as f:
        json.dump(config, f)

# Need to do this again because the earlier scope doesn't remain valid.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_motor1_pin, GPIO.OUT)
GPIO.setup(pwm_motor2_pin, GPIO.OUT)
GPIO.output(pwm_motor1_pin, False)
GPIO.output(pwm_motor2_pin, False)


if __name__ == '__main__':

    # Read the latest config variables
    with open('config.json') as f:
        config = json.load(f)

        DESIRED_PH_LOWER = float(config['DESIRED_PH_LOWER'])
        DESIRED_PH_UPPER = float(config['DESIRED_PH_UPPER'])
        WAIT_TIME = float(config['WAIT_TIME'])
        PUMP_DURATION = float(config['PUMP_DURATION'])

    print(f'Lower pH Bound: {DESIRED_PH_LOWER}, Upper pH Bound: {DESIRED_PH_UPPER}, Wait: {WAIT_TIME}s, Pump Duration: {PUMP_DURATION}')

    run_motor(motor=1, duration=PUMP_DURATION)

    # Need to do this again because the earlier scope doesn't remain valid.
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm_motor1_pin, GPIO.OUT)
    GPIO.setup(pwm_motor2_pin, GPIO.OUT)
    GPIO.output(pwm_motor1_pin, False)
    GPIO.output(pwm_motor2_pin, False)




