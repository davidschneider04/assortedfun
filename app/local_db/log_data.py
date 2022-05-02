import datetime
import sqlite3
import time

import adafruit_scd30
import board
import busio


con = sqlite3.connect('dadata.db')
cur = con.cursor()

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

# this will usually fail, it is easier to just keep it here
try:
    cur.execute('''CREATE TABLE temp (dttm TIMESTAMP, temp_f REAL);''')
except sqlite3.OperationalError:
    pass
try:
    cur.execute('''CREATE TABLE co2 (dttm TIMESTAMP, co2 REAL);''')
except sqlite3.OperationalError:
    pass
try:
    cur.execute('''CREATE TABLE humidity (dttm TIMESTAMP, humidity REAL);''')
except sqlite3.OperationalError:
    pass


def log_scd(cur, con, scd):
    while not scd.data_available:
        time.sleep(.5)
    dttm = datetime.datetime.now().strftime("%F %X")
    temp = ((scd.temperature)*(9/5)+32)
    cur.execute("INSERT INTO temp VALUES (:dttm, :temp)",
            {"dttm": dttm, "temp": temp})
    co2 = scd.CO2
    cur.execute("INSERT INTO co2 VALUES (:dttm, :co2)",
            {"dttm": dttm, "co2": co2})
    humidity = scd.relative_humidity
    cur.execute("INSERT INTO humidity VALUES (:dttm, :humidity)",
            {"dttm":dttm, "humidity": humidity})
    con.commit()


while True:
    log_scd(cur, con, scd)
    time.sleep(5)

cursor.close()
con.close()
