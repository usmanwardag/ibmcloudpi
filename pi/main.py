import adafruit_ads1x15.ads1015 as ADS
import Adafruit_DHT
import board
import busio
import json
import mh_z19
import time

from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
from pytz import timezone

from motors import run_motor
from actuators import set_light, set_humidifier, set_fan


### ADC Initialize ###
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads, ADS.P0)
tds_chan = AnalogIn(ads, ADS.P1)


### Config Variables ###
with open('/home/pi/ibmcloudpi/pi/config.json') as f:
    config = json.load(f)
    PUMP_DURATION = float(config['PUMP_DURATION'])
    DESIRED_PH_LOWER = float(config['DESIRED_PH_LOWER'])
    DESIRED_PH_UPPER = float(config['DESIRED_PH_UPPER'])
    DESIRED_EC_LOWER = float(config['DESIRED_EC_LOWER'])
    DESIRED_EC_UPPER = float(config['DESIRED_EC_UPPER'])
    DESIRED_HUMID_LOWER = float(config['DESIRED_HUMID_LOWER'])
    DESIRED_HUMID_UPPER = float(config['DESIRED_HUMID_UPPER'])
    DESIRED_TEMP_LOWER = float(config['DESIRED_TEMP_LOWER'])
    DESIRED_TEMP_UPPER = float(config['DESIRED_TEMP_UPPER'])
    LED_START_HOUR = float(config['LED_START_HOUR'])
    LED_END_HOUR = float(config['LED_END_HOUR'])


### Helper Functions ###
def convert_ph(adc_value):
    """ Given an adc value, get corresponding pH """

    # Calibrations
    # (x1, y1) -> Calibration pair 1
    # --      x1 -> ADC value, y1 -> Corresponding pH
    # (x2, y2) -> Calibration pair 2
    # --  x2 -> ADC value, y2 -> Corresponding pH
    x1, y1 = 2.5, 7
    x2, y2 = 2.04, 8

    # Calculate Slope and Intercept
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - (slope * x1)
    ph = (slope * adc_value) + intercept
    return ph


def convert_tds(tds_adc):
    # Output signal 0-2.3V
    # Corresponds to 0 - 1000ppm
    return tds_adc * 435

### --- End Helper Functions --- ###


### Sensor Read Functions ###
def get_ph():
    ph_adc = chan.voltage
    ph = convert_ph(ph_adc)
    return ph_adc, ph


def get_tds():
    tds_adc = tds_chan.voltage
    tds = convert_tds(tds_adc)
    return tds_adc, tds


def get_co2():
    info = mh_z19.read_all()
    return info['co2']


def get_temp():
    info = mh_z19.read_all()
    return info['temperature']


def get_humidity():
    sensor = Adafruit_DHT.DHT11
    gpio = 25
    humidity, temp = Adafruit_DHT.read_retry(sensor, gpio)
    return humidity

### --- End Sensor Read Functions --- ###

### Main Control Routine ###


def routine():

    tz = timezone('US/Eastern')
    curr_time = datetime.now(tz)

    _, pH = get_ph()
    _, tds = get_tds()
    co2 = get_co2()
    temp = get_temp()
    humidity = get_humidity()

    print(
        f'time: {curr_time}, pH: {round(pH, 2)}, TDS: {round(tds, 2)}, co2: {co2}, temp: {temp}, humidity: {humidity}')

    print(f'>> CONFIG - PH: {DESIRED_PH_LOWER}-{DESIRED_PH_UPPER}, EC: {DESIRED_EC_LOWER}-{DESIRED_EC_UPPER}, '
          f'C02: {DESIRED_HUMID_LOWER}-{DESIRED_HUMID_UPPER}, Light: {LED_START_HOUR}-{LED_END_HOUR}')

    # pH control
    if pH > DESIRED_PH_LOWER and pH < DESIRED_PH_UPPER:
        print('>> PH is within desired limits.')
    elif pH < DESIRED_PH_LOWER:
        # Run motor 2, which controls base
        print('>> Running motor 2, which controls base (to increase pH).')
        run_motor(motor=2, duration=PUMP_DURATION)
    elif pH > DESIRED_PH_UPPER:
        # Run motor 1, which controls acid
        print('>> Running motor 1, which controls acid (to decrease pH).')
        run_motor(motor=1, duration=PUMP_DURATION)

    # EC (Nutrient) control
    if tds > DESIRED_EC_LOWER and tds < DESIRED_EC_UPPER:
        print('>> EC is within desired limits.')
    elif tds < DESIRED_EC_LOWER:
        print('>> Running motors 3 and 4, which control nutrients.')
        # Motor 3 actually runs both motors 3 and 4 simultaneously
        run_motor(motor=3, duration=PUMP_DURATION)
    elif tds > DESIRED_EC_UPPER:
        print('>> ALERT! Add more water to dilute EC')

    # Humidity control
    if humidity > DESIRED_HUMID_LOWER and humidity < DESIRED_HUMID_UPPER:
        print('>> Humidity is within desired limits.')
    elif humidity < DESIRED_HUMID_LOWER:
        # Turn on humidifier 5 seconds
        print('>> Humidity is below limits. Turning humidifier ON for 5 seconds.')
        t = time.time()
        while (time.time() - t) < 5:
            set_humidifier(True)
        set_humidifier(False)
    elif humidity > DESIRED_HUMID_UPPER:
        # Turn on exhaust fan for 5 seconds
        print('>> Humidity is above limits. Turning exhaust fan ON for 5 seconds.')
        t = time.time()
        while (time.time() - t) < 5:
            set_fan(True)
        set_fan(False)

    # Light control
    if curr_time.hour >= LED_START_HOUR and curr_time.hour < LED_END_HOUR:
        print('>> Light ON.')
        set_light(True)
    else:
        print('>> Light OFF.')
        set_light(False)

    # Turn exhaust fan on for 10 seconds every 10 minutes
    if curr_time.minute % 10 == 0:
        print('>> Turning exhaust fan ON for 10 seconds.')
        t = time.time()
        while (time.time() - t) < 10:
            set_fan(True)
        set_fan(False)


if __name__ == '__main__':
    routine()
