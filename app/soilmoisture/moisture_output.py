# This example shows using TCA9548A to perform a simple scan for connected devices
from adafruit_seesaw.seesaw import Seesaw
import adafruit_tca9548a
import board
import busio
import time


i2c = board.I2C()  # uses board.SCL and board.SDA
nums = {1:'one',2:'two',3:'three',4:'four'}

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

for channel in range(8):
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = tca[channel].scan()
        print([hex(address) for address in addresses if address != 0x70])
        tca[channel].unlock()

# the multiplexer
tca = adafruit_tca9548a.TCA9548A(i2c)


soil_sensors = []
# create object for each sensor
for i in range(4):
    print(i)
    try:
        soil_sensor = Seesaw(tca[i+2], addr=0x36)
        soil_sensors.append(soil_sensor)
    except (OSError, ValueError) as e:
        print('this is a temporary wiring error')
    #soil_sensors = {nums[i+1]:Seesaw(tca[i+2], addr=0x36) for i in range(4)}

while True:
    for i, ss in enumerate(soil_sensors):
        moisture = ss.moisture_read()
        temp = ss.get_temp()
        print(f'sensor #{i}', f'temp: {temp}', f'moisture: {moisture}')
        print('\n')
    time.sleep(1)


