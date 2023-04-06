
import RPi.GPIO as GPIO 
from time import time, sleep

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


#pwm_motor1 = GPIO.PWM(pwm_motor1_pin, 5)
#pwm_motor2 = GPIO.PWM(pwm_motor2_pin, 5)



def set_rotation(direction='counter_clockwise'):
    if direction == 'clockwise':
        GPIO.output(rotation_1_pin, True)    
        GPIO.output(rotation_2_pin, False)
    elif direction == 'counter_clockwise':
        GPIO.output(rotation_1_pin, False)
        GPIO.output(rotation_2_pin, True)


def stop():
    print('In stop')
    pwm_motor1.stop()
    pwm_motor2.stop()
    sleep(2)

def run_motor_new(motor, duration, direction='counter_clockwise'):
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
            print('Starting Motor 1.')
            GPIO.output(pwm_motor1_pin, True)
        elif motor == 2:
            print('Starting Motor 2.')
            GPIO.output(pwm_motor2_pin, True)

    GPIO.output(pwm_motor1_pin, False)
    GPIO.output(pwm_motor2_pin, False)


def run_motor(motor, duration, direction='counter_clockwise'):
    """
    motor: int
        Which motor to run? 1 -> Motor 1, 2 -> Motor 2
    duration: float
        Time in seconds to run the motor
    """
    # Start with 0 so that it doesn't run yet.
    pwm_motor1.start(0)
    pwm_motor2.start(0)
    #pwm_motor1.stop()
    #pwm_motor2.stop()
    #exit()

    start_time = time()

    while (time() - start_time) < duration: 
        set_rotation(direction)
        # Change speed to 1%
        if motor == 1:
            print('Starting Motor 1.')
            pwm_motor1.ChangeDutyCycle(10)
            GPIO.output(pwm_motor1_pin, True)
        elif motor == 2:
            print('Starting Motor 2.')
            pwm_motor2.ChangeDutyCycle(10)
            GPIO.output(pwm_motor2_pin, True)

    """
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    pwm1 = GPIO.PWM(pwm_motor1_pin, 100)
    pwm2 = GPIO.PWM(pwm_motor2_pin, 100)

    print('Stopping motors.')
    GPIO.output(pwm_motor1_pin, False)
    GPIO.output(pwm_motor2_pin, False)
    pwm1.stop()
    pwm2.stop()
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()
    """

run_motor_new(motor=1, duration=0.1)
#sleep(5)
#print('Stopping')
#stop()
exit()

while True:
    try:
        # set_rotation(direction='clockwise')
        set_rotation(direction='counter_clockwise')
        pwm_motor1.ChangeDutyCycle(10)
        # pwm_motor2.ChangeDutyCycle(10)
        GPIO.output(pwm_motor1_pin, True)
    except KeyboardInterrupt:
        pwm_motor1.stop()
        pwm_motor2.stop()
        GPIO.cleanup()


