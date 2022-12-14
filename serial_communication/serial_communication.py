import serial
import time

communication_port = 'COM5'
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

gcode_file = 'star.gcode'

file = open(gcode_file, 'r')
lines = file.readlines()


def write_read(x):
    data = arduino.readline()
    if data == "> ":
        arduino.write(x.encode())
    print(x.encode)


# index = 0
for line in lines:
    write_read(line)
    # index += 1
