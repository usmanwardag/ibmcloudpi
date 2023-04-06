import time
import wiotp.sdk.application

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# ADC code from
# https://github.com/adafruit/Adafruit_Python_ADS1x15/blob/master/Adafruit_ADS1x15/ADS1x15.py

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2/3

# Calibrations
# (x1, y1) -> Calibration pair 1
#   x1 -> ADC value, y1 -> Corresponding pH
# (x2, y2) -> Calibration pair 2
#   x2 -> ADC value, y2 -> Corresponding pH
x1, y1 = 0.198, 7
x2, y2 = 0.173, 8.25


def convert_ph(adc_value):
    """ Given an adc value, get corresponding pH """
    # Calculate Slope and Intercept
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - (slope * x1)
    ph = (slope * adc_value) + intercept
    return ph


def get_ph():

    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)

    # Normalize
    ph_adc = values[0] / 65535
    ph = convert_ph(ph_adc)

    return ph_adc, ph

def publishAccCallback():
    print("pH Published.")


if __name__ == '__main__':

    options = wiotp.sdk.application.parseConfigFile("application.yaml")
    client = wiotp.sdk.application.ApplicationClient(config=options)
    client.connect()

    while True:
        _, pH = get_ph()
        print(f'Current pH: {pH}')
        client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="ph", msgFormat="json", data={'ph': pH}, onPublish=publishAccCallback)
        time.sleep(0.5)
