import serial
import time

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)


value_on = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]

value_off = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

while True:
    print("off")

    ser.write(serial.to_bytes(value_off))

    time.sleep(1)

    print("on")

    ser.write(serial.to_bytes(value_on))

    time.sleep(1)

    



