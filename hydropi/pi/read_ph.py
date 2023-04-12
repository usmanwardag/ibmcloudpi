import time
import wiotp.sdk.application

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
tds_chan = AnalogIn(ads, ADS.P1)


# Calibrations
# (x1, y1) -> Calibration pair 1
#   x1 -> ADC value, y1 -> Corresponding pH
# (x2, y2) -> Calibration pair 2
#   x2 -> ADC value, y2 -> Corresponding pH
x1, y1 = 2.5, 7
#x2, y2 = 3.37, 3.5
x2, y2 = 2.04, 8


def convert_ph(adc_value):
    """ Given an adc value, get corresponding pH """
    # Calculate Slope and Intercept
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - (slope * x1)
    ph = (slope * adc_value) + intercept
    return ph


def convert_tds(tds_adc):
    # Output signal 0-2.3V
    # Corresponds to 0 - 1000ppm
    return tds_adc * 435


def get_ph():

    # Read all the ADC channel values in a list.
    # Normalize
    ph_adc = chan.voltage
    print(f'Debug> Voltage: {ph_adc}')
    ph = convert_ph(ph_adc)

    return ph_adc, ph

def get_tds():
    tds_adc = tds_chan.voltage
    tds = convert_tds(tds_adc)
    return tds_adc, tds



if __name__ == '__main__':


    while True:
        _, pH = get_ph()
        print(f'Current pH: {pH}')

        tds_adc, tds = get_tds()
        print(f'Current TDS voltage: {tds_adc}, TDS: {tds}')

        time.sleep(0.5)
