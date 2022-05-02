import adafruit_scd30
import board
import busio
import time


i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        print(f"Self calibration: {scd.self_calibration_enabled}")
        print(f"Pressure: {scd.ambient_pressure}")
        print(f"Altitude: {scd.altitude}")
        print("Waiting for new data...")
        print("")

    time.sleep(0.5)

