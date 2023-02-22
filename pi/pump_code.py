
import RPi.GPIO as GPIO 
from time import time, sleep
from read_ph import get_ph 

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

DESIRED_PH_LOWER = 5.8
DESIRED_PH_UPPER = 6.5
WAIT_TIME = 30
PUMP_DURATION = 0.2


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


def adjust_ph(ph_low=DESIRED_PH_LOWER, ph_high=DESIRED_PH_UPPER):
    
    # Motor 1 -> Acid, Motor 2 -> Base

    while True:
        _, ph = get_ph()
        print(f'Current PH: {ph}')

        if ph > ph_low and ph < ph_high:
            print('PH is within desired limits.')
            break

        elif ph < ph_low:
            # Run motor 2, which controls base
            print('Running motor 2, which controls base (to increase pH).')
            run_motor(motor=2, duration=PUMP_DURATION)

        elif ph > ph_high:
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

        # Wait for 30 seconds for readings to become stable
        print(f'Sleeping for {WAIT_TIME} seconds')
        sleep(WAIT_TIME)
        
        


    #run_motor(motor=2, duration=10)

adjust_ph()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_motor1_pin, GPIO.OUT)
GPIO.setup(pwm_motor2_pin, GPIO.OUT)
GPIO.output(pwm_motor1_pin, False)
GPIO.output(pwm_motor2_pin, False)


