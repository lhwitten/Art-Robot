import serial
import time

communication_port = '/dev/tty.usbmodem141201'
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

gcode_file = 'straight_line_test.gcode.txt'

file = open(gcode_file,'r')
lines = file.readlines()

def write_read(x):
    arduino.write(x.encode())
    time.sleep(0.05)
    data = arduino.readline()
    return data


for line in lines:
    line = list(line)+[";"]
    write_read("".join(line))
