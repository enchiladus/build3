import serial
import time
import mariadb as mdb
from datetime import datetime

arduino = serial.Serial("/dev/ttyACM0", 9600)
data = int(arduino.readline())
time.sleep(1)
print(data)

con = mdb.connect(host='localhost',
                  user='root',
                  password='password', port=3306);
count = 0
lastValue = data
cursor =con.cursor()
while True:
    data = int(arduino.readline())
    print(data)
    if not lastValue == data:
        insert_value = 1 if data > 0 else 0
        cursor.execute("INSERT INTO build3.events(timestamp, value) VALUES (%s, %s)", (datetime.now(), insert_value))
        con.commit()
        lastValue = data
        count = count + 1
    time.sleep(1)
cursor.close()
