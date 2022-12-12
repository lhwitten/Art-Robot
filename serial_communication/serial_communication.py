import serial
import time

communication_port = 'COM8'
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

# gcode_file = "C:\Users\opidruchna\OneDrive - Olin College of Engineering\Documents\PIE\Art-Robot\serial_communication"

file = open(r"C:\\Users\\opidruchna\\OneDrive - Olin College of Engineering\Documents\\PIE\Art-Robot\serial_communication",'r')
lines = file.readlines()

def write_read(x):
    arduino.write(x.encode())
    time.sleep(0.05)
    data = arduino.readline()
    return data


for line in lines:
    write_read(line)
