import serial
import time

<<<<<<< HEAD
communication_port = '/dev/tty.usbmodem141201'
=======
communication_port = 'COM5'
>>>>>>> f0015221fb8a0ecfd75773e550ba2091391bac62
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

gcode_file = 'star.gcode'

file = open(r"C:\\Users\\opidruchna\\OneDrive - Olin College of Engineering\Documents\\PIE\Art-Robot\serial_communication", 'r')
lines = file.readlines()

<<<<<<< HEAD

def write_read(x):
=======
def write_read(x,index):
>>>>>>> f0015221fb8a0ecfd75773e550ba2091391bac62
    arduino.write(x.encode())
    if index != 1 and index != 2:
        time.sleep(4)
    else:
        time.sleep(4)
    data = 0
    #data = arduino.readline()
    return data

index = 0
for line in lines:
    index += 1
    data = write_read(line,index)
    print(index)
    print(data)
