import adafruit_si7021
from board import SCL, SDA
from busio import I2C


i2c = I2C(SCL, SDA)
sensor = adafruit_si7021.SI7021(i2c)


def to_fahrenheit(temp):
    """
    Convert temperature from default Celsius to Fahrenheit

    :field temp: The temperature value to convert
    :type temp: float
    :returns: Fahrenheit temperature value
    :rtype: float
    """
    fahr = ((temp*(9/5))+32)
    return fahr
