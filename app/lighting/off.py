import datetime

import adafruit_mcp4725
import board
import busio


i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

print(dac.value)
dac.normalized_value = 0
print(dac.value)
