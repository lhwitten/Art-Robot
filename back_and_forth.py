import serial
import time

communication_port = '/dev/tty.usbmodem143201'
arduino = serial.Serial(port=communication_port, baudrate=57600, timeout=1)

gcode_file = 'butterfly.gcode'

file = open(gcode_file, 'r')
lines = file.readlines()

total_commands = len(lines)
i = 0
while arduino.isOpen():
    data = arduino.readline().decode()
    print(data)
    if ">" in data and i < total_commands:
        msg = list(lines[i])
        if msg[-1] != ";":
            msg += [";"]
        msg = "".join(msg)
        arduino.write(msg.encode())
        print("command sent:" + msg)
        time.sleep(0.5)

        i += 1
