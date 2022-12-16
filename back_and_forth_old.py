import serial
import time

communication_port = '/dev/tty.usbmodem142301'
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

gcode_file = 'butterfly.gcode'

file = open(gcode_file, 'r')
lines = file.readlines()

total_commands = len(lines)
i = 0
while arduino.isOpen():
    data = arduino.readline().decode()
    print("from arduino ", data)
    if ">" in data and i < total_commands:
        # msg = list(lines[i])
        # msg = "".join(msg)
        lines[i] = lines[i].strip('\n')
        arduino.write(lines[i].encode())
        print("command sent:" + lines[i])
        time.sleep(0.01)

        i += 1