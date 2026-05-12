import serial
import time
import subprocess
import serial
import time
import os

ser = serial.Serial(
                  'COM7',
                  baudrate = 9600,
                  parity=serial.PARITY_NONE,
                  stopbits=serial.STOPBITS_ONE,
                  bytesize=serial.EIGHTBITS,                  
                  timeout=1
                  )

time.sleep(2) #give the connection a second to settle
print('waiting for vehicle')
while True:
    d = ser.readline()
    d = d.decode('UTF-8', 'ignore')
    d = d.strip()
    if d:
        print(d)
        if os.path.exists('slot.txt'):
            os.remove('slot.txt')

        if d == 'entry':
            print("Entry.........")
            subprocess.Popen(["python", "Entrycode.py"])
            while True:
                if os.path.exists('slot.txt'):
                    f = open('slot.txt', 'r')
                    slot = f.read()     
                    f.close()
                    ser.write(str.encode(slot))  # Encode string to bytes
                    break
                time.sleep(0.5)
            time.sleep(0.5)

        if d == 'exit':
            print("Exit..........")
            subprocess.Popen(["python", "Exitcode.py"])
            while True:
                if os.path.exists('slot.txt'):
                    f = open('slot.txt', 'r')
                    slot = f.read()     
                    f.close()
                    ser.write(str.encode(slot))  # Encode string to bytes
                    break
                time.sleep(0.5)
            time.sleep(0.5)
    time.sleep(1)
